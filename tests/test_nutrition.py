import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT / "services" / "nutrition-service"))

from bmr import calculate_bmr
from goal import adjust_calories
from macros import calculate_macros
from tdee import calculate_tdee


def test_bmr_calculation_male():
    result = calculate_bmr(70, 175, 30, "male")
    assert round(result, 2) == 1648.75


def test_tdee_calculation():
    assert calculate_tdee(1600, 1.55) == 2480.0


def test_goal_adjustment_lose():
    assert adjust_calories(2500, "lose") == 2000.0


def test_macros_total_non_negative():
    macros = calculate_macros(75, 2200)
    assert macros["protein_g"] > 0
    assert macros["fat_g"] > 0
    assert macros["carbs_g"] >= 0
