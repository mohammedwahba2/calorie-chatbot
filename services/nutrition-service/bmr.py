def calculate_bmr(weight: float, height: float, age: int, gender: str) -> float:
    s = 5 if gender.lower() == "male" else -161
    return round((10 * weight) + (6.25 * height) - (5 * age) + s, 2)
