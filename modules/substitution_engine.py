import re

# measurement & noise words (never ingredients)
STOP_WORDS = {
    "tsp","tsps","teaspoon","teaspoons",
    "tbsp","tbsps","tablespoon","tablespoons",
    "cup","cups","lb","lbs","pound","pounds",
    "oz","ounce","ounces","can","cans",
    "large","small","medium","scant",
    "fresh","ground","chopped","sliced",
    "cloves","clove","dash","to","taste",
    "and","or","of"
}

SUBSTITUTION_MAP = {
    "beef": ["soy chunks", "mushroom"],
    "chicken": ["paneer", "tofu"],
    "butter": ["oil"],
    "milk": ["soy milk", "almond milk"],
    "egg": ["tofu", "flaxseed"],
    "soy sauce": ["salt"],
    "cheddar": ["mozzarella"]
}

def normalize_ingredient(text):
    """
    Extracts core ingredient name from noisy text.
    """
    text = text.lower()

    # remove numbers & fractions
    text = re.sub(r"[\d/]+", " ", text)

    # remove punctuation
    text = re.sub(r"[^\w\s]", " ", text)

    words = [
        w for w in text.split()
        if w not in STOP_WORDS and len(w) > 2
    ]

    # keep only first 1–2 meaningful words
    return " ".join(words[:2])


def analyze_ingredients(recipe_ingredients, user_ingredients):
    recipe_clean = {normalize_ingredient(i) for i in recipe_ingredients}
    user_clean = {normalize_ingredient(i) for i in user_ingredients}

    missing = recipe_clean - user_clean
    extra = user_clean - recipe_clean

    substitutes = {
        m: SUBSTITUTION_MAP[m]
        for m in missing
        if m in SUBSTITUTION_MAP
    }

    return missing, extra, substitutes
