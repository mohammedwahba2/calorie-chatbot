from __future__ import annotations

import re

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models import ChatSession, HealthProfile, Message, User
from app.schemas import ChatRequest, ChatResponse
from app.services.ai_service import detect_language, extract_user_data, generate_ai_response
from app.services.authz import get_current_user
from app.services.nutrition_service import calculate_nutrition
from app.services.session_store import REQUIRED_FIELDS, get_state

router = APIRouter(tags=["chat"])


@router.post("/chat/sessions")
def create_chat_session(payload: dict, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    session_id = payload.get("session_id")
    if not session_id:
        return {"detail": "session_id is required"}

    existing = db.query(ChatSession).filter(
        ChatSession.session_id == session_id,
        ChatSession.user_id == user.id,
    ).first()
    if existing:
        return {"session_id": existing.session_id, "created": False}

    session = ChatSession(session_id=session_id, user_id=user.id)
    db.add(session)
    db.commit()
    return {"session_id": session_id, "created": True}


@router.get("/chat/sessions")
def chat_sessions(
    limit: int = Query(default=20, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    base_query = db.query(ChatSession).filter(ChatSession.user_id == user.id)
    total = base_query.count()
    sessions = base_query.order_by(ChatSession.id.desc()).offset(offset).limit(limit).all()
    result = []
    for session in sessions:
        last_message = (
            db.query(Message)
            .filter(Message.session_id == session.id)
            .order_by(Message.id.desc())
            .first()
        )
        result.append(
            {
                "session_id": session.session_id,
                "language": session.language,
                "last_message": last_message.content[:120] if last_message else "",
                "updated_at": (
                    (last_message.created_at.isoformat() if last_message and last_message.created_at else "")
                    or (session.created_at.isoformat() if session.created_at else "")
                ),
            }
        )
    return {
        "items": result,
        "total": total,
        "limit": limit,
        "offset": offset,
    }


@router.get("/chat/history/{session_id}")
def chat_history(session_id: str, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    session = db.query(ChatSession).filter(
        ChatSession.session_id == session_id,
        ChatSession.user_id == user.id,
    ).first()
    if not session:
        return []

    rows = db.query(Message).filter(Message.session_id == session.id).order_by(Message.id.asc()).all()
    return [
        {
            "role": row.role,
            "content": row.content,
            "timestamp": row.created_at.isoformat() if row.created_at else "",
        }
        for row in rows
    ]


@router.post("/chat", response_model=ChatResponse)
def chat(payload: ChatRequest, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    session = db.query(ChatSession).filter(
        ChatSession.session_id == payload.session_id,
        ChatSession.user_id == user.id,
    ).first()
    if not session:
        session = ChatSession(session_id=payload.session_id, user_id=user.id)
        db.add(session)
        db.commit()
        db.refresh(session)

    state_key = f"{user.id}:{payload.session_id}"
    state = get_state(state_key)
    if state["language"] is None:
        state["language"] = detect_language(payload.message)
    language = state["language"]

    extracted = extract_user_data(payload.message, language)

    normalized_msg = payload.message.translate(str.maketrans("٠١٢٣٤٥٦٧٨٩", "0123456789"))
    single_number_match = re.fullmatch(r"\s*(\d{1,3})\s*", normalized_msg)
    if single_number_match:
        number_value = int(single_number_match.group(1))
        pending_numeric = [field for field in ["weight", "height", "age"] if state["data"].get(field) is None]
        if pending_numeric:
            field = pending_numeric[0]
            if field == "weight" and 30 <= number_value <= 350:
                extracted["weight"] = number_value
            elif field == "height" and 100 <= number_value <= 250:
                extracted["height"] = number_value
            elif field == "age" and 10 <= number_value <= 100:
                extracted["age"] = number_value

    for key, value in extracted.items():
        if value is not None:
            state["data"][key] = value

    missing = [field for field in REQUIRED_FIELDS if state["data"].get(field) is None]

    db.add(Message(session_id=session.id, role="user", content=payload.message))

    history_rows = db.query(Message).filter(Message.session_id == session.id).order_by(Message.id.asc()).all()
    history = [{"role": row.role, "content": row.content} for row in history_rows]

    coach_context = {
        "language": language,
        "goal": state["data"].get("goal"),
        "weight": state["data"].get("weight"),
        "height": state["data"].get("height"),
        "age": state["data"].get("age"),
        "activity_level": state["data"].get("activity_level"),
        "missing_fields": missing,
        "already_asked": sorted(list(state["asked"])),
    }

    if missing:
        field_to_ask = missing[0]
        state["asked"].add(field_to_ask)
        coach_context["focus_field"] = field_to_ask
        reply = generate_ai_response(payload.message, coach_context, history)
    else:
        nutrition = calculate_nutrition(state["data"])
        coach_context["nutrition"] = nutrition
        coach_context["adaptive_plan"] = "Update calories each week based on 7-day average weight trend"
        coach_context["daily_reminder"] = (
            "اشرب مياه كفاية وسجل اكلك" if language == "ar" else "Drink enough water and log your meals"
        )

        reply = generate_ai_response(payload.message, coach_context, history)

        profile = db.query(HealthProfile).filter(HealthProfile.user_id == user.id).first()
        if not profile:
            profile = HealthProfile(user_id=user.id)

        profile.weight = float(state["data"]["weight"])
        profile.height = float(state["data"]["height"])
        profile.age = int(state["data"]["age"])
        profile.activity_level = state["data"]["activity_level"]
        profile.goal = state["data"]["goal"]
        db.add(profile)

    db.add(Message(session_id=session.id, role="assistant", content=reply))
    session.language = language
    db.add(session)
    db.commit()

    return ChatResponse(reply=reply, language=language, missing_fields=missing, profile=state["data"])
