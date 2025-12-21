🍳 VoiceChef AI – Voice-Controlled Cooking Assistant

VoiceChef AI is a multimodal AI cooking assistant that helps users find recipes, follow step-by-step cooking instructions, manage cooking time, analyze ingredients, and estimate nutrition — using voice and text interaction.
This project is built as a B.Tech AIML resume-worthy mini project using only free tools and beginner-friendly logic.
-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
🎯 Project Objective

To design an AI system that:
Accepts voice or text input for recipes
Guides users through step-by-step cooking
Provides voice instructions
Manages cooking time using a smart timer
Suggests ingredient substitutions
Estimates nutritional values
Demonstrates real-world use of Speech + NLP + Python AI
----------------------------------------------------------------------------------------------
✨ Key Features

🎤 Voice Input (Speech-to-Text)
Speak the dish name instead of typing.
📖 Recipe Retrieval Engine
Fetches recipes from a real-world dataset.
👨‍🍳 Step-by-Step Cooking Guide
Clear and structured cooking instructions.
🔊 Voice Cooking Guide (Text-to-Speech)
Reads cooking steps aloud using browser-based audio.
⏲️ Smart Cooking Timer
Automatically detects time from instructions (e.g., “cook for 10 minutes”).
🔁 Ingredient Analysis & Substitution
Identifies missing and extra ingredients and suggests alternatives.
🥗 Nutrition Analysis
Estimates calories, protein, carbohydrates, and fat.
🖥️ Interactive Streamlit Dashboard
Simple and clean UI suitable for demos and evaluation.
----------------------------------------------------------------------------------------------
🛠️ Tech Stack

Language: Python
UI: Streamlit
Speech-to-Text: SpeechRecognition
Text-to-Speech: gTTS
NLP & Logic: Python, Regex
Data Handling: Pandas, NumPy
ML (Lightweight): scikit-learn
Datasets: CSV-based (Recipes & Nutrition)
----------------------------------------------------------------------------------------------
📂 Project Structure

VoiceChef_AI/
│
├── app.py
├── requirements.txt
├── README.md
│
├── modules/
│   ├── speech_to_text.py
│   ├── recipe_engine.py
│   ├── text_to_speech.py
│   ├── timer_engine.py
│   ├── substitution_engine.py
│   └── nutrition_engine.py
│
├── data/
│   ├── recipes.csv        (not included in repo)
│   └── nutrition.csv      (not included in repo)

----------------------------------------------------------------------------------------------
📊 Dataset Information

⚠️ Large datasets are not included in this repository due to GitHub size limits.

Please download them manually and place inside the data/ folder.

Recipe Dataset:
https://www.kaggle.com/datasets/shuyangli94/food-com-recipes-and-user-interactions

Nutrition Dataset:
https://www.kaggle.com/datasets/niharika41298/nutrition-details-for-most-common-foods
----------------------------------------------------------------------------------------------
▶️ How to Run the Project
1️⃣ Clone the Repository
git clone https://github.com/Noureesh2305/VoiceChef-AI.git
cd VoiceChef-AI

2️⃣ Create Virtual Environment (Optional)
python -m venv venv
venv\Scripts\activate   # Windows

3️⃣ Install Dependencies
pip install -r requirements.txt

4️⃣ Add Datasets

Place downloaded CSV files inside:

data/

5️⃣ Run the Application
streamlit run app.py
----------------------------------------------------------------------------------------------
🧪 How to Use

Enter or speak a dish name
View ingredients and cooking steps
Click Read Step for voice guidance
Use Start Timer for timed steps
Analyze ingredient availability
View nutrition summary
----------------------------------------------------------------------------------------------
🔮 Future Enhancements (Optional)

Auto-refresh timers
Multilingual voice support
Personalized diet recommendations
User login & recipe history
Advanced nutrition modeling
----------------------------------------------------------------------------------------------
👤 Author

Shaik Noureesh
B.Tech – Artificial Intelligence & Machine Learning
