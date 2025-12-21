import pandas as pd

# Load dataset
nutrition_df = pd.read_csv("data/nutrition.csv")

# Normalize column names
nutrition_df.columns = [c.lower() for c in nutrition_df.columns]

# Convert numeric columns safely
numeric_cols = ["calories", "protein", "fat", "carbs"]

for col in numeric_cols:
    nutrition_df[col] = pd.to_numeric(nutrition_df[col], errors="coerce").fillna(0)


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
        # Take first meaningful word
        key = ing.lower().split()[0]

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
