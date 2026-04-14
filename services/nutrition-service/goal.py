def adjust_calories(tdee: float, goal: str) -> float:
    normalized = goal.lower()
    if normalized == "lose":
        return round(tdee - 500, 2)
    if normalized == "gain":
        return round(tdee + 350, 2)
    return round(tdee, 2)
