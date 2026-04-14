from __future__ import annotations

conversation_state: dict[str, dict] = {}


REQUIRED_FIELDS = ["goal", "weight", "height", "age", "activity_level"]


def get_state(state_key: str) -> dict:
    if state_key not in conversation_state:
        conversation_state[state_key] = {
            "language": None,
            "data": {
                "goal": None,
                "weight": None,
                "height": None,
                "age": None,
                "activity_level": None,
            },
            "asked": set(),
        }
    return conversation_state[state_key]
