from __future__ import annotations


def activity_factor(level: str) -> float:
    mapping = {"low": 1.2, "moderate": 1.55, "high": 1.725}
    return mapping.get(level, 1.2)


def calculate_nutrition(profile: dict) -> dict:
    weight = float(profile["weight"])
    height = float(profile["height"])
    age = int(profile["age"])
    goal = profile["goal"]
    factor = activity_factor(profile["activity_level"])

    bmr = (10 * weight) + (6.25 * height) - (5 * age) + 5
    tdee = bmr * factor
    if goal == "lose":
        calories = tdee - 500
    elif goal == "gain":
        calories = tdee + 300
    else:
        calories = tdee

    protein_g = round(weight * 1.8, 1)
    fat_g = round((calories * 0.27) / 9, 1)
    carbs_g = round(max((calories - protein_g * 4 - fat_g * 9) / 4, 0), 1)

    return {
        "bmr": round(bmr, 2),
        "tdee": round(tdee, 2),
        "calories": round(calories, 2),
        "protein_g": protein_g,
        "carbs_g": carbs_g,
        "fat_g": fat_g,
    }
