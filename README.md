# VoiceChef AI

VoiceChef AI is a Streamlit cooking assistant that helps users search recipes, follow step-by-step cooking instructions, hear cooking guidance aloud, manage timers, check available ingredients, find substitutions, and estimate nutrition.

This project is designed as a B.Tech AIML mini project using Python, Streamlit, speech tools, recipe data, and beginner-friendly AI/NLP logic.

## Project Objective

VoiceChef AI demonstrates a practical AI assistant that can:

- Accept text or voice input for recipe search
- Retrieve recipes from a local dataset
- Guide users through cooking one step at a time
- Read cooking steps aloud
- Detect cooking times from recipe instructions
- Suggest substitutions for missing ingredients
- Estimate nutritional values
- Present everything in an interactive Streamlit dashboard

## Features

- Recipe search over the local recipe dataset
- Multiple recipe matches with a selector
- Guided cooking mode with previous and next controls
- Step progress indicator
- Text-to-speech for the current cooking step
- Timer detection from steps such as `5 minutes`, `30 seconds`, or `1 hour`
- Ingredient availability checker
- Substitute suggestions for common missing ingredients
- Nutrition estimate for calories, protein, carbs, and fat
- Cached recipe search to avoid repeatedly scanning the large CSV
- Graceful text-to-speech warning if `gTTS` is not installed

## Tech Stack

- Python
- Streamlit
- Pandas and NumPy
- SpeechRecognition
- gTTS
- Regex-based NLP logic
- CSV recipe and nutrition datasets

## Project Structure

```text
VoiceChef_AI/
├── app.py
├── requirements.txt
├── README.md
├── test_datasets.py
├── data/
│   ├── recipes.csv
│   └── nutrition.csv
└── modules/
    ├── nutrition_engine.py
    ├── recipe_engine.py
    ├── speech_to_text.py
    ├── substitution_engine.py
    ├── text_to_speech.py
    └── timer_engine.py
```

## Dataset Information

Large datasets are not included in this repository due to GitHub size limits.

Download the datasets manually and place them inside the `data/` folder:

- Recipe dataset: https://www.kaggle.com/datasets/shuyangli94/food-com-recipes-and-user-interactions
- Nutrition dataset: https://www.kaggle.com/datasets/niharika41298/nutrition-details-for-most-common-foods

Expected local files:

```text
data/
├── recipes.csv
└── nutrition.csv
```

## Setup

Clone the repository:

```powershell
git clone https://github.com/Noureesh2305/VoiceChef-AI.git
cd VoiceChef-AI
```

Create and activate a virtual environment:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

Install dependencies:

```powershell
pip install -r requirements.txt
```

Run the app:

```powershell
streamlit run app.py
```

## How To Use

1. Enter or speak a dish name.
2. Choose one of the matching recipes.
3. Review the ingredients.
4. Add the ingredients you already have to check missing items.
5. Use the guided cooking panel to move through each step.
6. Click `Read step` for audio guidance.
7. Start a detected timer when a step includes cooking time.
8. Analyze nutrition to view estimated calories, protein, carbs, and fat.

## Notes

- `data/recipes.csv` can be very large, so recipe search is chunked and cached instead of loading the entire file when the app starts.
- Voice input uses the local microphone through `speechrecognition` and `pyaudio`.
- Text-to-speech uses `gTTS`, so step audio needs an internet connection.
- Nutrition values are estimates based on partial ingredient matching.

## Quick Dataset Check

To confirm both CSV files can be read:

```powershell
python test_datasets.py
```

## Future Enhancements

- Auto-refreshing timers
- Multilingual voice support
- Personalized diet recommendations
- User recipe history
- Advanced nutrition modeling
- Favorite recipes and shopping list export

## Author

Shaik Noureesh  
B.Tech - Artificial Intelligence & Machine Learning
