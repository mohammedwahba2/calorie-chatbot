from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from meal_engine import build_recommendation

app = FastAPI(title="Recommendation Service", version="2.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)


class RecommendationRequest(BaseModel):
    weight: float = Field(gt=0)
    height: float = Field(gt=0)
    age: int = Field(gt=0)
    gender: str = "male"
    activity_level: float = Field(gt=0)
    goal: str


@app.post("/recommend")
def recommend(payload: RecommendationRequest):
    return build_recommendation(
        weight=payload.weight,
        height=payload.height,
        age=payload.age,
        gender=payload.gender,
        activity_level=payload.activity_level,
        goal=payload.goal,
    )
