# test_datasets.py
import pandas as pd

recipes = pd.read_csv("data/recipes.csv")
nutrition = pd.read_csv("data/nutrition.csv")

print("Recipes dataset shape:", recipes.shape)
print("Recipes columns:", recipes.columns)

print("\nNutrition dataset shape:", nutrition.shape)
print("Nutrition columns:", nutrition.columns)
