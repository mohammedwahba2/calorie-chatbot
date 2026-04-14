from __future__ import annotations

import re
from typing import Any

ARABIC_DIGITS = str.maketrans("٠١٢٣٤٥٦٧٨٩", "0123456789")

STEPS = [
    "start",
    "ask_goal",
    "ask_weight",
    "ask_height",
    "ask_age",
    "ask_activity",
    "calculate_plan",
    "done",
]

PROMPTS = {
    "en": {
        "ask_goal": "Great to meet you. What is your goal: lose, gain, or maintain weight?",
        "ask_weight": "Got it. What is your current weight in kg?",
        "ask_height": "Thanks. What is your height in cm?",
        "ask_age": "Perfect. How old are you?",
        "ask_activity": "How active are you: low, moderate, or high?",
        "invalid_goal": "Please type one goal only: lose, gain, or maintain.",
        "invalid_number": "Please enter a valid number.",
        "invalid_activity": "Please choose one activity level: low, moderate, or high.",
        "followup": "If you want, I can adjust the plan based on your feedback.",
    },
    "ar": {
        "ask_goal": "اهلا بيك. هدفك ايه: تخس، تزود، ولا تحافظ على الوزن؟",
        "ask_weight": "تمام. كام وزنك الحالي بالكيلو؟",
        "ask_height": "ممتاز. كام طولك بالسنتيمتر؟",
        "ask_age": "حلو. عندك كام سنة؟",
        "ask_activity": "مستوى نشاطك ايه: قليل، متوسط، ولا عالي؟",
        "invalid_goal": "اكتب هدف واحد فقط: تخس، تزود، او تحافظ.",
        "invalid_number": "من فضلك اكتب رقم صحيح.",
        "invalid_activity": "اختار مستوى نشاط واحد: قليل، متوسط، او عالي.",
        "followup": "لو حابب اقدر اعدل الخطة حسب ملاحظاتك.",
    },
}


def detect_language(text: str) -> str:
    return "ar" if re.search(r"[\u0600-\u06FF]", text) else "en"


def normalize_text(text: str) -> str:
    return text.strip().lower().translate(ARABIC_DIGITS)


def parse_goal(text: str) -> str | None:
    normalized = normalize_text(text)
    if re.search(r"\blose\b|weight loss|اخس|خس|تنحيف", normalized):
        return "lose"
    if re.search(r"\bgain\b|bulk|زيادة|ازيد|تخن", normalized):
        return "gain"
    if re.search(r"\bmaintain\b|ثبات|احافظ|حافظ", normalized):
        return "maintain"
    return None


def parse_number(text: str, minimum: int, maximum: int) -> int | None:
    normalized = normalize_text(text)
    match = re.search(r"(\d{1,3})", normalized)
    if not match:
        return None
    value = int(match.group(1))
    if value < minimum or value > maximum:
        return None
    return value


def parse_activity(text: str) -> tuple[str, float] | None:
    normalized = normalize_text(text)
    if re.search(r"\blow\b|sedentary|قليل|خفيف", normalized):
        return ("low", 1.2)
    if re.search(r"\bmoderate\b|متوسط|جيم", normalized):
        return ("moderate", 1.55)
    if re.search(r"\bhigh\b|نشيط|عالي|heavy", normalized):
        return ("high", 1.725)
    return None


def calculate_plan(data: dict[str, Any]) -> dict[str, Any]:
    weight = float(data["weight"])
    height = float(data["height"])
    age = int(data["age"])
    activity_level = float(data["activity_level"])
    goal = data["goal"]

    bmr = (10 * weight) + (6.25 * height) - (5 * age) + 5
    tdee = bmr * activity_level
    if goal == "lose":
        calories = tdee - 500
    elif goal == "gain":
        calories = tdee + 350
    else:
        calories = tdee

    protein = weight * 1.8
    fat = (calories * 0.27) / 9
    carbs = max((calories - (protein * 4) - (fat * 9)) / 4, 0)

    return {
        "bmr": round(bmr, 2),
        "tdee": round(tdee, 2),
        "calories": round(calories, 2),
        "protein": round(protein, 1),
        "carbs": round(carbs, 1),
        "fat": round(fat, 1),
    }


def suggestion(language: str, goal: str) -> str:
    if language == "ar":
        if goal == "lose":
            return "ركز على البروتين والخضار وقلل السكريات قدر الامكان."
        if goal == "gain":
            return "زود وجباتك تدريجيا مع مصادر كارب معقدة وبروتين عالي."
        return "حافظ على توازن الوجبات وجودة النوم والنشاط اليومي."

    if goal == "lose":
        return "Prioritize lean protein, vegetables, and reduce sugary snacks."
    if goal == "gain":
        return "Increase meals gradually with quality carbs and enough protein."
    return "Keep a balanced plate, stable activity, and consistent sleep."


def build_plan_reply(language: str, plan: dict[str, Any], goal: str) -> str:
    if language == "ar":
        return (
            f"خلاص جهزت خطتك. سعراتك اليومية حوالي {int(plan['calories'])} كالوري. "
            f"بروتين {plan['protein']}جم، كارب {plan['carbs']}جم، دهون {plan['fat']}جم. "
            f"{suggestion(language, goal)}"
        )

    return (
        f"Your plan is ready. Target calories: {int(plan['calories'])} kcal/day. "
        f"Protein: {plan['protein']}g, Carbs: {plan['carbs']}g, Fat: {plan['fat']}g. "
        f"{suggestion(language, goal)}"
    )
