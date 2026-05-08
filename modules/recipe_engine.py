import ast
import re
from functools import lru_cache
from pathlib import Path

import pandas as pd


DATA_PATH = Path(__file__).resolve().parent.parent / "data" / "recipes.csv"
RECIPE_COLUMNS = ["title", "ingredients", "directions", "link", "source"]


def normalize_query(text):
    return re.sub(r"\s+", " ", str(text).lower()).strip()


def _safe_list(value):
    if isinstance(value, list):
        return value

    if pd.isna(value):
        return []

    try:
        parsed = ast.literal_eval(str(value))
    except (SyntaxError, ValueError):
        return []

    if isinstance(parsed, list):
        return [str(item).strip() for item in parsed if str(item).strip()]

    return []


def _clean_recipe(row):
    ingredients = _safe_list(row.get("ingredients"))
    directions = [
        step
        for step in _safe_list(row.get("directions"))
        if len(step.strip()) > 3 and not step.lower().strip().startswith("serves")
    ]

    return {
        "title": str(row.get("title", "Untitled recipe")).strip(),
        "ingredients": ingredients,
        "directions": directions,
        "link": str(row.get("link", "") or "").strip(),
        "source": str(row.get("source", "") or "").strip(),
    }


@lru_cache(maxsize=64)
def search_recipes(query, limit=12):
    """
    Search recipes by title without loading the multi-GB CSV into memory.
    Results are cached per query for fast repeated searches in Streamlit.
    """
    query = normalize_query(query)
    if not query:
        return []

    matches = []
    query_tokens = [token for token in query.split() if len(token) > 1]

    try:
        chunks = pd.read_csv(
            DATA_PATH,
            usecols=RECIPE_COLUMNS,
            chunksize=25_000,
            low_memory=False,
        )
    except FileNotFoundError:
        return []

    for chunk in chunks:
        titles = chunk["title"].fillna("").astype(str).str.lower()
        mask = titles.str.contains(re.escape(query), na=False)

        if not mask.any() and query_tokens:
            mask = titles.apply(lambda title: all(token in title for token in query_tokens))

        if mask.any():
            for _, row in chunk.loc[mask].head(limit - len(matches)).iterrows():
                recipe = _clean_recipe(row)
                if recipe["ingredients"] and recipe["directions"]:
                    matches.append(recipe)

        if len(matches) >= limit:
            break

    return matches


def get_recipe(user_query):
    matches = search_recipes(user_query, limit=1)
    return matches[0] if matches else None
