from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models import Meal, User
from app.schemas import MealLogRequest
from app.services.authz import get_current_user

router = APIRouter(prefix="/meals", tags=["meals"])


@router.post("/log")
def log_meal(payload: MealLogRequest, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    meal = Meal(
        user_id=user.id,
        session_public_id=payload.session_id,
        meal_type=payload.meal_type,
        description=payload.description,
        calories=payload.calories,
        protein_g=payload.protein_g,
        carbs_g=payload.carbs_g,
        fat_g=payload.fat_g,
    )
    db.add(meal)
    db.commit()
    db.refresh(meal)

    return {
        "id": meal.id,
        "meal_type": meal.meal_type,
        "description": meal.description,
        "calories": meal.calories,
        "protein_g": meal.protein_g,
        "carbs_g": meal.carbs_g,
        "fat_g": meal.fat_g,
        "logged_at": meal.logged_at.isoformat() if meal.logged_at else "",
    }


@router.get("/log")
def list_meals(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    meals = db.query(Meal).filter(Meal.user_id == user.id).order_by(Meal.id.desc()).limit(30).all()
    return [
        {
            "id": meal.id,
            "meal_type": meal.meal_type,
            "description": meal.description,
            "calories": meal.calories,
            "protein_g": meal.protein_g,
            "carbs_g": meal.carbs_g,
            "fat_g": meal.fat_g,
            "logged_at": meal.logged_at.isoformat() if meal.logged_at else "",
        }
        for meal in meals
    ]
