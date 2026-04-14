from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from bmr import calculate_bmr
from goal import adjust_calories
from macros import calculate_macros
from schemas import UserInput
from tdee import calculate_tdee

app = FastAPI(title="Nutrition Service", version="2.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)


@app.post("/calculate")
def calculate(user: UserInput):
    bmr = calculate_bmr(user.weight, user.height, user.age, user.gender)
    tdee = calculate_tdee(bmr, user.activity_level)
    target_calories = adjust_calories(tdee, user.goal)
    macros = calculate_macros(user.weight, target_calories)

    return {
        "bmr": bmr,
        "tdee": tdee,
        "target_calories": target_calories,
        "macros": macros,
    }
