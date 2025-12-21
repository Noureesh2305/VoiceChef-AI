import pandas as pd
import ast

recipes_df = pd.read_csv("data/recipes.csv")

def get_recipe(user_query):
    if not user_query:
        return None

    query = user_query.lower()

    matches = recipes_df[
        recipes_df["title"].str.lower().str.contains(query, na=False)
    ]

    if matches.empty:
        return None

    row = matches.iloc[0]

    ingredients = ast.literal_eval(row["ingredients"])
    directions = ast.literal_eval(row["directions"])

    return {
        "title": row["title"],
        "ingredients": ingredients,
        "directions": directions
    }
