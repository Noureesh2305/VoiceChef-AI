import html
import time

import streamlit as st

from modules.nutrition_engine import analyze_nutrition
from modules.recipe_engine import search_recipes
from modules.speech_to_text import get_voice_input
from modules.substitution_engine import analyze_ingredients
from modules.text_to_speech import speak
from modules.timer_engine import extract_time, format_seconds, start_timer


st.set_page_config(page_title="VoiceChef AI", layout="wide")


st.markdown(
    """
    <style>
        .block-container {
            padding-top: 1.6rem;
            padding-bottom: 2rem;
            max-width: 1180px;
        }
        .app-title {
            font-size: 2.35rem;
            font-weight: 800;
            margin-bottom: .2rem;
        }
        .app-subtitle {
            color: #5f6368;
            font-size: 1.02rem;
            margin-bottom: 1.3rem;
        }
        .step-card {
            border: 1px solid #e8eaed;
            border-radius: 8px;
            padding: 1.25rem 1.35rem;
            background: #ffffff;
            min-height: 190px;
        }
        .step-text {
            font-size: 1.35rem;
            line-height: 1.65;
            color: #202124;
        }
        .small-muted {
            color: #6b7280;
            font-size: .9rem;
        }
        div[data-testid="stMetricValue"] {
            font-size: 1.45rem;
        }
    </style>
    """,
    unsafe_allow_html=True,
)


def init_state():
    defaults = {
        "query": "",
        "matches": [],
        "recipe": None,
        "last_recipe": None,
        "step_index": 0,
        "timer_end": None,
        "timer_running": False,
        "nutrition": None,
        "ingredient_text": "",
    }
    for key, value in defaults.items():
        st.session_state.setdefault(key, value)


def get_steps(recipe):
    return [
        step.strip()
        for step in recipe.get("directions", [])
        if len(step.strip()) > 3 and not step.lower().strip().startswith("serves")
    ]


@st.cache_data(show_spinner=False, ttl=3600)
def cached_search(query):
    return search_recipes(query, limit=10)


@st.cache_data(show_spinner=False)
def cached_nutrition(ingredients):
    return analyze_nutrition(list(ingredients))


def reset_for_recipe(recipe):
    st.session_state.recipe = recipe
    st.session_state.last_recipe = recipe.get("title")
    st.session_state.step_index = 0
    st.session_state.timer_end = None
    st.session_state.timer_running = False
    st.session_state.nutrition = None


def move_step(delta):
    recipe = st.session_state.recipe
    if not recipe:
        return

    steps = get_steps(recipe)
    st.session_state.step_index = min(
        max(st.session_state.step_index + delta, 0),
        max(len(steps) - 1, 0),
    )
    st.session_state.timer_end = None
    st.session_state.timer_running = False


init_state()

st.markdown('<div class="app-title">VoiceChef AI</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="app-subtitle">Search a dish, check your ingredients, and cook one guided step at a time.</div>',
    unsafe_allow_html=True,
)

search_col, cook_col = st.columns([0.38, 0.62], gap="large")

with search_col:
    st.markdown("#### Find a recipe")
    with st.container(border=True):
        use_voice = st.button("Speak", use_container_width=True)
        voice_search = False

        if use_voice:
            with st.spinner("Listening..."):
                spoken = get_voice_input()
            if spoken:
                st.session_state.query = spoken
                voice_search = True
                st.success(f"Heard: {spoken}")
            else:
                st.warning("Could not understand the audio.")

        st.text_input(
            "Dish name",
            key="query",
            placeholder="Try chicken pasta, brownies, tomato soup",
        )

        run_search = st.button("Search", type="primary", use_container_width=True) or voice_search

        if run_search:
            if st.session_state.query.strip():
                with st.spinner("Searching recipes..."):
                    st.session_state.matches = cached_search(st.session_state.query)
                if st.session_state.matches:
                    reset_for_recipe(st.session_state.matches[0])
                else:
                    st.session_state.recipe = None
                    st.warning("No matching recipes found. Try a shorter dish name.")
            else:
                st.info("Enter a dish name to search.")

        if st.session_state.matches:
            labels = [
                f"{idx + 1}. {recipe['title']}"
                for idx, recipe in enumerate(st.session_state.matches)
            ]
            selected_label = st.selectbox("Choose recipe", labels)
            selected_index = labels.index(selected_label)
            selected_recipe = st.session_state.matches[selected_index]
            if (
                not st.session_state.recipe
                or selected_recipe["title"] != st.session_state.recipe.get("title")
            ):
                reset_for_recipe(selected_recipe)

    recipe = st.session_state.recipe
    if recipe:
        st.markdown("#### Ingredients")
        with st.container(border=True):
            for ingredient in recipe.get("ingredients", [])[:24]:
                st.write(f"- {ingredient}")
            if len(recipe.get("ingredients", [])) > 24:
                st.caption(f"+ {len(recipe['ingredients']) - 24} more")

        st.markdown("#### Ingredient check")
        with st.container(border=True):
            st.text_area(
                "What you have",
                key="ingredient_text",
                placeholder="onion, oil, salt, chicken",
                height=96,
            )
            if st.session_state.ingredient_text.strip():
                user_ingredients = [
                    item.strip()
                    for item in st.session_state.ingredient_text.split(",")
                    if item.strip()
                ]
                missing, extra, substitutes = analyze_ingredients(
                    recipe.get("ingredients", []),
                    user_ingredients,
                )

                if missing:
                    st.warning(f"Missing: {', '.join(missing)}")
                else:
                    st.success("You have the main ingredients.")

                if substitutes:
                    st.markdown("Substitutes")
                    for ingredient, options in substitutes.items():
                        st.write(f"- {ingredient}: {', '.join(options)}")

                if extra:
                    st.caption(f"Extra: {', '.join(extra)}")

        st.markdown("#### Nutrition estimate")
        with st.container(border=True):
            if st.button("Analyze nutrition", use_container_width=True):
                st.session_state.nutrition = cached_nutrition(
                    tuple(recipe.get("ingredients", []))
                )

            if st.session_state.nutrition:
                n = st.session_state.nutrition
                c1, c2 = st.columns(2)
                c1.metric("Calories", f"{n['calories']} kcal")
                c2.metric("Protein", f"{n['protein']} g")
                c3, c4 = st.columns(2)
                c3.metric("Carbs", f"{n['carbs']} g")
                c4.metric("Fat", f"{n['fat']} g")
                st.caption("Estimate based on partial ingredient matching.")

with cook_col:
    recipe = st.session_state.recipe

    if not recipe:
        st.markdown("#### Ready when you are")
        st.info("Search for a dish to start guided cooking.")
    else:
        steps = get_steps(recipe)
        total_steps = len(steps)
        current_index = min(st.session_state.step_index, max(total_steps - 1, 0))
        st.session_state.step_index = current_index

        st.markdown(f"### {recipe['title']}")
        source_bits = [bit for bit in [recipe.get("source"), recipe.get("link")] if bit]
        if source_bits:
            st.caption(" | ".join(source_bits))

        if not steps:
            st.error("This recipe does not include usable cooking directions.")
        else:
            progress = (current_index + 1) / total_steps
            st.progress(progress, text=f"Step {current_index + 1} of {total_steps}")

            current_step = steps[current_index]
            current_step_html = html.escape(current_step)
            st.markdown(
                f"""
                <div class="step-card">
                    <div class="small-muted">Current step</div>
                    <div class="step-text">{current_step_html}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

            detected_time = extract_time(current_step)
            st.write("")

            nav_prev, nav_read, nav_timer, nav_next = st.columns([1, 1, 1, 1])
            with nav_prev:
                st.button(
                    "Previous",
                    disabled=current_index == 0,
                    on_click=move_step,
                    args=(-1,),
                    use_container_width=True,
                )
            with nav_read:
                if st.button("Read step", use_container_width=True):
                    try:
                        with st.spinner("Preparing audio..."):
                            audio = speak(current_step)
                        st.audio(audio, format="audio/mp3")
                    except RuntimeError as exc:
                        st.warning(str(exc))
            with nav_timer:
                if detected_time:
                    if st.button(
                        f"Timer {format_seconds(detected_time)}",
                        use_container_width=True,
                    ):
                        st.session_state.timer_end = start_timer(detected_time)
                        st.session_state.timer_running = True
                else:
                    st.button("No timer", disabled=True, use_container_width=True)
            with nav_next:
                next_label = "Finish" if current_index == total_steps - 1 else "Next"
                if st.button(next_label, type="primary", use_container_width=True):
                    if current_index == total_steps - 1:
                        st.success("Cooking completed. Enjoy your meal!")
                        try:
                            audio = speak("Cooking completed. Enjoy your meal!")
                            st.audio(audio, format="audio/mp3")
                        except RuntimeError as exc:
                            st.warning(str(exc))
                    else:
                        move_step(1)
                        st.rerun()

            if st.session_state.timer_running and st.session_state.timer_end:
                remaining = int(st.session_state.timer_end - time.time())
                if remaining > 0:
                    st.warning(f"Time remaining: {format_seconds(remaining)}")
                    st.caption("Use Refresh timer to update the countdown.")
                    if st.button("Refresh timer"):
                        st.rerun()
                else:
                    st.session_state.timer_running = False
                    st.success("Time completed.")
                    try:
                        audio = speak("Time is up")
                        st.audio(audio, format="audio/mp3")
                    except RuntimeError as exc:
                        st.warning(str(exc))

            st.markdown("#### All steps")
            with st.container(border=True):
                for idx, step in enumerate(steps):
                    marker = "Current" if idx == current_index else f"Step {idx + 1}"
                    st.markdown(f"**{marker}.** {step}")
