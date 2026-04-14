from __future__ import annotations

from rules import (
    extract_activity,
    extract_age,
    extract_gender,
    extract_goal,
    extract_height,
    extract_weight,
    normalize_text,
)


def parse_user_input(text: str) -> dict:
    normalized = normalize_text(text)

    activity = extract_activity(normalized)

    result = {
        "weight": extract_weight(normalized),
        "height": extract_height(normalized),
        "age": extract_age(normalized),
        "goal": extract_goal(normalized),
        "gender": extract_gender(normalized),
        "activity": activity["activity"] if activity else None,
        "activity_level": activity["activity_level"] if activity else None,
    }

    return result
