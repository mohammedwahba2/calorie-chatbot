from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models import HealthProfile, User
from app.services.authz import get_current_user

router = APIRouter(tags=["profile"])


@router.get("/me")
def me(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    profile = db.query(HealthProfile).filter(HealthProfile.user_id == user.id).first()
    return {
        "email": user.email,
        "profile": {
            "weight": profile.weight if profile else None,
            "height": profile.height if profile else None,
            "age": profile.age if profile else None,
            "activity_level": profile.activity_level if profile else None,
            "goal": profile.goal if profile else None,
        },
    }
