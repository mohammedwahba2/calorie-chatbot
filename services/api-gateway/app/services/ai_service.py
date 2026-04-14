from __future__ import annotations

import json
import re
from typing import Any

import requests

from app.core.config import OLLAMA_MODEL, OLLAMA_URL


def detect_language(text: str) -> str:
    return "ar" if re.search(r"[\u0600-\u06FF]", text) else "en"


def ask_ollama(prompt: str, temperature: float = 0.3) -> str:
    try:
        response = requests.post(
            OLLAMA_URL,
            json={
                "model": OLLAMA_MODEL,
                "prompt": prompt,
                "stream": False,
                "options": {"temperature": temperature},
            },
            timeout=60,
        )
        response.raise_for_status()
        body = response.json()
        return (body.get("response") or "").strip()
    except Exception:
        return ""


def generate_ai_response(user_input: str, user_context: dict[str, Any], history: list[dict[str, str]]) -> str:
    language = user_context.get("language") or detect_language(user_input)
    history_text = "\n".join([f"{m['role']}: {m['content']}" for m in history[-8:]])

    prompt = f"""
You are an elite AI nutrition coach.
Language: {language}
You must reply in the same language.

User profile context:
{json.dumps(user_context, ensure_ascii=False)}

Conversation history:
{history_text}

Latest user message:
{user_input}

Rules:
- Ask only one next best question if profile is missing fields.
- Never ask duplicate questions already answered.
- If all required data is available, provide dynamic personalized coaching:
  - calories
  - macros
  - breakfast/lunch/dinner ideas
  - motivational advice
  - one adaptive suggestion based on habits
- Keep response practical, empathetic, and concise.
"""
    response = ask_ollama(prompt, temperature=0.55)
    if response:
        return response

    language = user_context.get("language", "en")
    missing = user_context.get("missing_fields") or []
    nutrition = user_context.get("nutrition")
    if missing:
        field = missing[0]
        fallback_questions = {
            "en": {
                "goal": "What is your goal: lose, gain, or maintain?",
                "weight": "What is your current weight in kg?",
                "height": "What is your height in cm?",
                "age": "How old are you?",
                "activity_level": "How active are you: low, moderate, or high?",
            },
            "ar": {
                "goal": "ايه هدفك: تخس ولا تزود ولا تحافظ؟",
                "weight": "كام وزنك الحالي بالكيلو؟",
                "height": "كام طولك بالسنتيمتر؟",
                "age": "عندك كام سنة؟",
                "activity_level": "مستوى نشاطك ايه: قليل ولا متوسط ولا عالي؟",
            },
        }
        return fallback_questions[language][field]

    if nutrition:
        if language == "ar":
            return (
                f"سعراتك اليومية المناسبة حوالي {int(nutrition['calories'])} كالوري. "
                f"بروتين {nutrition['protein_g']} جم، كارب {nutrition['carbs_g']} جم، دهون {nutrition['fat_g']} جم. "
                "خطة يومية: فطار بيض وشوفان، غدا دجاج ورز، عشا زبادي وسلطة. استمر وسجل وجباتك يوميا."
            )
        return (
            f"Your daily target is around {int(nutrition['calories'])} kcal. "
            f"Protein {nutrition['protein_g']}g, carbs {nutrition['carbs_g']}g, fat {nutrition['fat_g']}g. "
            "Daily plan: eggs and oats for breakfast, chicken and rice for lunch, yogurt and salad for dinner. Keep going and log meals consistently."
        )

    return "Let's continue your coaching journey." if language == "en" else "نكمل الرحلة الصحية خطوة بخطوة."


def extract_user_data(message: str, language: str) -> dict:
    prompt = f"""
Extract structured health data from this message.
Return JSON only with keys: goal, weight, height, age, activity_level.
Allowed values:
- goal: lose, gain, maintain, null
- activity_level: low, moderate, high, null
- weight/height/age: numbers or null
Language: {language}
Message: {message}
"""
    parsed = {}
    try:
        raw = ask_ollama(prompt, temperature=0)
        parsed = json.loads(raw)
    except Exception:
        parsed = {}

    fallback = fallback_extract(message)
    merged = {
        "goal": parsed.get("goal") if isinstance(parsed, dict) else None,
        "weight": parsed.get("weight") if isinstance(parsed, dict) else None,
        "height": parsed.get("height") if isinstance(parsed, dict) else None,
        "age": parsed.get("age") if isinstance(parsed, dict) else None,
        "activity_level": parsed.get("activity_level") if isinstance(parsed, dict) else None,
    }

    for key, value in fallback.items():
        if merged.get(key) is None and value is not None:
            merged[key] = value

    return merged


def fallback_extract(text: str) -> dict:
    normalized = text.lower().translate(str.maketrans("٠١٢٣٤٥٦٧٨٩", "0123456789"))

    goal = None
    if re.search(r"lose|اخس|تنحيف|خس", normalized):
        goal = "lose"
    elif re.search(r"gain|bulk|ازيد|زيادة", normalized):
        goal = "gain"
    elif re.search(r"maintain|ثبات|حافظ", normalized):
        goal = "maintain"

    activity = None
    if re.search(r"low|sedentary|قليل|خفيف", normalized):
        activity = "low"
    elif re.search(r"moderate|متوسط|جيم", normalized):
        activity = "moderate"
    elif re.search(r"high|heavy|عالي|نشيط", normalized):
        activity = "high"

    weight = None
    weight_match = re.search(r"(?:weight|وزن|kg|كيلو)\D{0,8}(\d{2,3})|(\d{2,3})\s?(?:kg|كيلو)", normalized)
    if weight_match:
        v = int(weight_match.group(1) or weight_match.group(2))
        if 30 <= v <= 350:
            weight = v

    height = None
    height_match = re.search(r"(?:height|طول|cm|سم)\D{0,8}(\d{2,3})|(\d{2,3})\s?(?:cm|سم)", normalized)
    if height_match:
        v = int(height_match.group(1) or height_match.group(2))
        if 100 <= v <= 250:
            height = v

    age = None
    age_match = re.search(r"(?:age|سن|year|سنة)\D{0,8}(\d{1,3})|(\d{1,3})\s?(?:year|سنة)", normalized)
    if age_match:
        v = int(age_match.group(1) or age_match.group(2))
        if 10 <= v <= 100:
            age = v

    return {
        "goal": goal,
        "activity_level": activity,
        "weight": weight,
        "height": height,
        "age": age,
    }
