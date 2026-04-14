from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models import ProgressLog, User
from app.schemas import ProgressLogRequest
from app.services.ai_service import generate_ai_response
from app.services.authz import get_current_user

router = APIRouter(tags=["progress"])


@router.post("/progress")
def add_progress(payload: ProgressLogRequest, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    log = ProgressLog(user_id=user.id, weight=payload.weight, note=payload.note)
    db.add(log)
    db.commit()
    db.refresh(log)

    return {
        "id": log.id,
        "weight": log.weight,
        "note": log.note,
        "logged_at": log.logged_at.isoformat() if log.logged_at else "",
    }


@router.get("/progress")
def get_progress(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    logs = db.query(ProgressLog).filter(ProgressLog.user_id == user.id).order_by(ProgressLog.id.asc()).all()
    avg_weight = round(sum(item.weight for item in logs) / len(logs), 2) if logs else None

    history = [{"role": "user", "content": f"Weight log {item.weight} kg"} for item in logs[-7:]]
    insight = ""
    if logs:
        context = {
            "language": "en",
            "goal": "progress",
            "weight_average": avg_weight,
            "log_count": len(logs),
            "missing_fields": [],
        }
        try:
            insight = generate_ai_response("Give adaptive weekly guidance", context, history)
        except Exception:
            insight = "Keep consistency, track meals daily, and adjust calories weekly based on your weight trend."

    return {
        "logs": [
            {
                "id": item.id,
                "weight": item.weight,
                "note": item.note,
                "logged_at": item.logged_at.isoformat() if item.logged_at else "",
            }
            for item in logs
        ],
        "average_weight": avg_weight,
        "insight": insight,
        "daily_reminder": "Log your meals and water intake before bedtime.",
    }
