from pathlib import Path

import pandas as pd

DATA_PATH = Path(__file__).resolve().parent.parent / "data" / "nutrition.csv"

nutrition_df = pd.read_csv(DATA_PATH)

# Normalize column names
nutrition_df.columns = [c.lower() for c in nutrition_df.columns]

# Convert numeric columns safely
numeric_cols = ["calories", "protein", "fat", "carbs"]

for col in numeric_cols:
    nutrition_df[col] = pd.to_numeric(nutrition_df[col], errors="coerce").fillna(0)


def _ingredient_key(text):
    words = [
        word
        for word in str(text).lower().replace(",", " ").split()
        if len(word) > 2 and not any(char.isdigit() for char in word)
    ]
    return words[-1] if words else ""


def analyze_nutrition(recipe_ingredients):
    """
    Estimate nutrition values using partial ingredient matching.
    """

    total = {
        "calories": 0.0,
        "protein": 0.0,
        "fat": 0.0,
        "carbs": 0.0
    }

    for ing in recipe_ingredients:
        key = _ingredient_key(ing)
        if not key:
            continue

        match = nutrition_df[
            nutrition_df["food"].str.lower().str.contains(key, na=False)
        ]

        if not match.empty:
            row = match.iloc[0]
            total["calories"] += float(row["calories"])
            total["protein"] += float(row["protein"])
            total["fat"] += float(row["fat"])
            total["carbs"] += float(row["carbs"])

    # Round nicely for UI
    return {k: round(v, 2) for k, v in total.items()}
