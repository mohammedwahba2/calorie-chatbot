from __future__ import annotations

from state_machine import STEPS

user_sessions: dict[str, dict] = {}


def default_session() -> dict:
    return {
        "step": STEPS[0],
        "language": None,
        "data": {
            "goal": None,
            "weight": None,
            "height": None,
            "age": None,
            "activity": None,
            "activity_level": None,
        },
    }


def get_user_session(session_id: str) -> dict:
    if session_id not in user_sessions:
        user_sessions[session_id] = default_session()
    return user_sessions[session_id]
