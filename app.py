import streamlit as st
import time

from modules.speech_to_text import get_voice_input
from modules.recipe_engine import get_recipe
from modules.text_to_speech import speak   # gTTS-based
from modules.timer_engine import extract_time
from modules.substitution_engine import analyze_ingredients
from modules.nutrition_engine import analyze_nutrition


st.set_page_config(page_title="VoiceChef AI", layout="centered")
st.title("🍳 VoiceChef AI – Voice Cooking Guide")


# ================= SESSION STATE =================
if "recipe" not in st.session_state:
    st.session_state.recipe = None

if "steps" not in st.session_state:
    st.session_state.steps = []
    st.session_state.step_index = 0

if "last_recipe" not in st.session_state:
    st.session_state.last_recipe = None

if "timer_end" not in st.session_state:
    st.session_state.timer_end = None

if "timer_running" not in st.session_state:
    st.session_state.timer_running = False


# ================= INPUT =================
st.markdown("### 🔎 Recipe Input")

text_query = st.text_input(
    "Type dish name (recommended):",
    placeholder="e.g., pasta, chicken, lasagna"
)

if st.button("🎤 Speak"):
    spoken = get_voice_input()
    if spoken:
        text_query = spoken
        st.success(f"You said: {spoken}")
    else:
        st.warning("❌ Could not understand audio")

if text_query:
    st.session_state.recipe = get_recipe(text_query)


# ================= DISPLAY =================
if st.session_state.recipe:
    recipe = st.session_state.recipe

    st.subheader(recipe["title"])

    # -------- INGREDIENTS --------
    st.markdown("### 🧂 Ingredients")
    for ing in recipe["ingredients"]:
        st.write("•", ing)

    # -------- STEP INIT --------
    if st.session_state.last_recipe != recipe["title"]:
        st.session_state.steps = [
            s for s in recipe["directions"]
            if len(s.strip()) > 5 and not s.lower().startswith("serves")
        ]
        st.session_state.step_index = 0
        st.session_state.timer_running = False
        st.session_state.timer_end = None
        st.session_state.last_recipe = recipe["title"]

    # ================= COOKING GUIDE =================
    st.markdown("### 👨‍🍳 Cooking Guide")

    current_step = st.session_state.steps[st.session_state.step_index]
    st.write(current_step)

    # ---- READ STEP ----
    read_key = f"read_{st.session_state.last_recipe}_{st.session_state.step_index}"
    if st.button("🔊 Read Step", key=read_key):
        audio = speak(current_step)
        st.audio(audio, format="audio/mp3")

    # ---- TIMER ----
    t = extract_time(current_step)

    if t and st.button("⏲️ Start Timer"):
        st.session_state.timer_end = time.time() + t
        st.session_state.timer_running = True

    if st.session_state.timer_running:
        remaining = int(st.session_state.timer_end - time.time())

        if remaining > 0:
            st.warning(f"⏳ Time remaining: {remaining} seconds")
            st.caption("🔄 Click anywhere to refresh timer")
        else:
            audio = speak("Time is up")
            st.audio(audio, format="audio/mp3")
            st.success("⏰ Time completed!")
            st.session_state.timer_running = False

    # ---- NEXT STEP ----
    if len(st.session_state.steps) > 1:
        if st.button("➡️ Next Step"):
            if st.session_state.step_index < len(st.session_state.steps) - 1:
                st.session_state.step_index += 1
                st.session_state.timer_running = False
            else:
                audio = speak("Cooking completed. Enjoy your meal!")
                st.audio(audio, format="audio/mp3")
                st.success("🎉 Cooking completed!")
    else:
        st.info("ℹ️ This recipe has a single cooking step.")

    # ================= INGREDIENT ANALYSIS =================
    st.markdown("### 🔁 Ingredient Analysis")

    have = st.text_input(
        "Ingredients you have (comma-separated):",
        placeholder="oil, onion, salt"
    )

    if have and have.strip():
        user_ings = [i.strip() for i in have.split(",") if i.strip()]
        recipe_ings = recipe["ingredients"]

        missing, extra, substitutes = analyze_ingredients(recipe_ings, user_ings)

        if missing:
            st.warning(f"❌ Missing ingredients: {', '.join(missing)}")
        else:
            st.success("✅ All required ingredients are available")

        if extra:
            st.info(f"ℹ️ Extra ingredients not used: {', '.join(extra)}")

        if substitutes:
            st.markdown("### 🔁 Suggested Substitutes")
            for k, v in substitutes.items():
                st.write(f"• {k} → {', '.join(v)}")

    # ================= NUTRITION =================
    st.markdown("### 🥗 Nutrition Analysis")

    if st.button("📊 Analyze Nutrition"):
        n = analyze_nutrition(recipe["ingredients"])
        st.write(f"🔥 Calories: {n['calories']} kcal")
        st.write(f"💪 Protein: {n['protein']} g")
        st.write(f"🍞 Carbs: {n['carbs']} g")
        st.write(f"🧈 Fat: {n['fat']} g")

else:
    st.info("👆 Enter or speak a dish name to begin cooking.")
