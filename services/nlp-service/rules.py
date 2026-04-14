from __future__ import annotations

import re
from typing import Any

AR_TO_EN_DIGITS = str.maketrans("٠١٢٣٤٥٦٧٨٩", "0123456789")

ACTIVITY_MAP = {
    "sedentary": 1.2,
    "light": 1.375,
    "moderate": 1.55,
    "active": 1.725,
    "very_active": 1.9,
}


GOAL_PATTERNS = {
    "lose": [r"\blose\b", r"weight loss", r"اخس", r"خس", r"تنحيف"],
    "gain": [r"\bgain\b", r"bulk", r"ازيد", r"زيادة", r"تخن", r"ضخامة"],
    "maintain": [r"\bmaintain\b", r"ثبات", r"حافظ"],
}

ACTIVITY_PATTERNS = {
    "very_active": [r"very active", r"athlete", r"مرتين يوم", r"رياضي محترف"],
    "active": [r"active", r"6 days", r"5 days", r"نشيط", r"شديد"],
    "moderate": [r"moderate", r"3 days", r"4 days", r"جيم", r"متوسط"],
    "light": [r"light", r"1 day", r"2 days", r"خفيف"],
    "sedentary": [r"sedentary", r"desk", r"قليل الحركة", r"مفيش تمرين"],
}


def normalize_text(text: str) -> str:
    return text.strip().lower().translate(AR_TO_EN_DIGITS)


def _extract_number(text: str, patterns: list[str], minimum: int, maximum: int) -> int | None:
    for pattern in patterns:
        match = re.search(pattern, text, flags=re.IGNORECASE)
        if match:
            value = int(match.group(1))
            if minimum <= value <= maximum:
                return value
    return None


def extract_weight(text: str) -> int | None:
    return _extract_number(
        text,
        [r"(?:weight|وزن(?:ي)?)\D{0,8}(\d{2,3})", r"(\d{2,3})\s?(?:kg|كيلو)"],
        minimum=30,
        maximum=350,
    )


def extract_height(text: str) -> int | None:
    return _extract_number(
        text,
        [r"(?:height|طول(?:ي)?)\D{0,8}(\d{2,3})", r"(\d{2,3})\s?(?:cm|سم)"],
        minimum=100,
        maximum=250,
    )


def extract_age(text: str) -> int | None:
    return _extract_number(
        text,
        [r"(?:age|سن(?:ي)?)\D{0,8}(\d{1,3})", r"(\d{1,3})\s?(?:year|سنة)"],
        minimum=10,
        maximum=100,
    )


def extract_goal(text: str) -> str | None:
    for goal, patterns in GOAL_PATTERNS.items():
        if any(re.search(pattern, text, flags=re.IGNORECASE) for pattern in patterns):
            return goal
    return None


def extract_activity(text: str) -> dict[str, Any] | None:
    for level, patterns in ACTIVITY_PATTERNS.items():
        if any(re.search(pattern, text, flags=re.IGNORECASE) for pattern in patterns):
            return {"activity": level, "activity_level": ACTIVITY_MAP[level]}
    return None


def extract_gender(text: str) -> str | None:
    if re.search(r"\bmale\b|ذكر|راجل", text, flags=re.IGNORECASE):
        return "male"
    if re.search(r"\bfemale\b|انثى|ست", text, flags=re.IGNORECASE):
        return "female"
    return None
