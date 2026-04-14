def calculate_macros(weight: float, calories: float):
    protein_g = weight * 1.8
    fat_g = (calories * 0.27) / 9

    protein_cal = protein_g * 4
    fat_cal = fat_g * 9
    carbs_g = max((calories - protein_cal - fat_cal) / 4, 0)

    return {
        "protein_g": round(protein_g, 2),
        "fat_g": round(fat_g, 2),
        "carbs_g": round(carbs_g, 2),
    }
