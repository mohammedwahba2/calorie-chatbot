from __future__ import annotations

import random

PROTEINS = ["chicken breast", "eggs", "greek yogurt", "lentils", "salmon", "cottage cheese"]
CARBS = ["oats", "brown rice", "quinoa", "sweet potato", "whole wheat bread", "pasta"]
FATS = ["avocado", "olive oil", "almonds", "peanut butter", "walnuts", "tahini"]
VEGGIES = ["spinach", "broccoli", "mixed salad", "cucumber", "tomatoes", "zucchini"]
FRUITS = ["banana", "apple", "berries", "orange", "dates", "mango"]


def calculate_bmr(weight: float, height: float, age: int, gender: str) -> float:
    sex_factor = 5 if gender.lower() == "male" else -161
    return round((10 * weight) + (6.25 * height) - (5 * age) + sex_factor, 2)


def calculate_tdee(bmr: float, activity_level: float) -> float:
    return round(bmr * activity_level, 2)


def adjust_goal_calories(tdee: float, goal: str) -> float:
    normalized_goal = goal.lower()
    if normalized_goal == "lose":
        return round(tdee - 500, 2)
    if normalized_goal == "gain":
        return round(tdee + 350, 2)
    return round(tdee, 2)


def calculate_macros(weight: float, target_calories: float) -> dict:
    protein_g = round(weight * 1.8, 2)
    fat_g = round((target_calories * 0.27) / 9, 2)
    carbs_g = round(max((target_calories - (protein_g * 4) - (fat_g * 9)) / 4, 0), 2)
    return {"protein_g": protein_g, "carbs_g": carbs_g, "fat_g": fat_g}


def _meal_text(name: str, protein: str, carb: str, fat: str, side: str, calories: int) -> dict:
    return {
        "name": name,
        "items": [protein, carb, fat, side],
        "estimated_calories": calories,
    }


def recommend_meals(target_calories: float, macros: dict) -> dict:
    rng = random.Random(int(target_calories + macros["protein_g"]))

    breakfast_cal = int(target_calories * 0.3)
    lunch_cal = int(target_calories * 0.4)
    dinner_cal = int(target_calories * 0.3)

    breakfast = _meal_text(
        "Breakfast",
        rng.choice(["eggs", "greek yogurt", "cottage cheese"]),
        rng.choice(["oats", "whole wheat bread"]),
        rng.choice(["peanut butter", "almonds", "tahini"]),
        rng.choice(FRUITS),
        breakfast_cal,
    )

    lunch = _meal_text(
        "Lunch",
        rng.choice(PROTEINS),
        rng.choice(CARBS),
        rng.choice(["olive oil", "avocado", "walnuts"]),
        rng.choice(VEGGIES),
        lunch_cal,
    )

    dinner = _meal_text(
        "Dinner",
        rng.choice(PROTEINS),
        rng.choice(CARBS),
        rng.choice(FATS),
        rng.choice(VEGGIES),
        dinner_cal,
    )

    return {
        "target_calories": round(target_calories, 2),
        "macro_targets": macros,
        "plan": {
            "breakfast": breakfast,
            "lunch": lunch,
            "dinner": dinner,
        },
    }


def build_recommendation(weight: float, height: float, age: int, gender: str, activity_level: float, goal: str) -> dict:
    bmr = calculate_bmr(weight, height, age, gender)
    tdee = calculate_tdee(bmr, activity_level)
    target_calories = adjust_goal_calories(tdee, goal)
    macros = calculate_macros(weight, target_calories)
    plan = recommend_meals(target_calories, macros)
    return {
        "nutrition": {
            "bmr": bmr,
            "tdee": tdee,
            "target_calories": target_calories,
            "macros": macros,
        },
        "recommendations": plan,
    }
