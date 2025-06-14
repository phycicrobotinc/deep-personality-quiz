import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import io

# ---------------------- INIT STATE ----------------------
if "submitted" not in st.session_state:
    st.session_state.submitted = False
if "answers" not in st.session_state:
    st.session_state.answers = {}
if "username" not in st.session_state:
    st.session_state.username = ""
if "reset_requested" not in st.session_state:
    st.session_state.reset_requested = False

# ---------------------- QUESTIONS ----------------------
questions = {
    1: "What is your gender?",
    2: "What is your age group?",
    3: "What is your current employment status?",
    4: "What is your approximate annual income?",
    5: "What is your favorite way to spend weekends?",
    6: "Red or Black?",
    7: "Do you consider yourself more introverted or extroverted?",
    8: "Do you enjoy trying new experiences?",
    9: "Red or Black?",
    10: "Are you more analytical or creative?",
    11: "Do you prefer working alone or in a team?",
    12: "Red or Black?",
    13: "Are you more spontaneous or planned?",
    14: "How often do you set long-term goals?",
    15: "Red or Black?",
    16: "Do you often reflect on your emotions?",
    17: "How important is financial security to you?",
    18: "Red or Black?",
    19: "Do you make decisions quickly or after lots of thought?",
    20: "What drives you most in life?"
}

options = {
    1: {"A": "Male", "B": "Female", "C": "Other", "D": "Prefer not to say"},
    2: {"A": "Under 18", "B": "18-24", "C": "25-34", "D": "35-44", "E": "45+"},
    3: {"A": "Employed full-time", "B": "Part-time", "C": "Student", "D": "Unemployed", "E": "Retired"},
    4: {"A": "<20k", "B": "20k-50k", "C": "50k-100k", "D": ">100k"},
    5: {"A": "Reading/relaxing", "B": "Sports", "C": "Socializing", "D": "Creative hobbies"},
    6: {"R": "Red", "B": "Black"},
    7: {"A": "Introverted", "B": "Extroverted"},
    8: {"A": "Love new experiences", "B": "Sometimes", "C": "Rarely"},
    9: {"R": "Red", "B": "Black"},
    10: {"A": "Analytical", "B": "Creative", "C": "Balanced"},
    11: {"A": "Alone", "B": "Team"},
    12: {"R": "Red", "B": "Black"},
    13: {"A": "Spontaneous", "B": "Planned"},
    14: {"A": "Often", "B": "Sometimes", "C": "Rarely"},
    15: {"R": "Red", "B": "Black"},
    16: {"A": "Yes", "B": "Sometimes", "C": "Not much"},
    17: {"A": "Very", "B": "Somewhat", "C": "Not important"},
    18: {"R": "Red", "B": "Black"},
    19: {"A": "Quickly", "B": "After thought"},
    20: {"A": "Success", "B": "Happiness", "C": "Growth", "D": "Peace"}
}

# ---------------------- ANALYZE PERSONALITY ----------------------
def analyze_personality(answers):
    red_count = sum(1 for q in answers if answers[q] == "R")
    black_count = sum(1 for q in answers if answers[q] == "B")

    traits = []
    if red_count > black_count:
        traits.append("bold")
    elif black_count > red_count:
        traits.append("calm")
    else:
        traits.append("balanced")

    if answers.get(7) == "A":
        traits.append("introspective")
    if answers.get(8) == "A":
        traits.append("curious")
    if answers.get(13) == "A":
        traits.append("spontaneous")
    if answers.get(14) == "A":
        traits.append("goal-oriented")

    if "bold" in traits and "curious" in traits:
        personality = "Explorer"
    elif "calm" in traits and "goal-oriented" in traits:
        personality = "Strategist"
    elif "spontaneous" in traits and "curious" in traits:
        personality = "Adventurer"
    else:
        personality = "Observer"

    description = f"You are a {personality}! This means you're {', '.join(traits)}."
    return personality, description

# ---------------------- RESET FUNCTION ----------------------
def reset_quiz():
    st.session_state.answers = {}
    st.session_state.username = ""
    st.session_state.submitted = False

# ---------------------- MAIN APP ----------------------
st.title("🧠 Deep Personality Quiz")

# Username input with reset on submit
username = st.text_input("Enter your name:", value=st.session_state.username)
if username != st.session_state.username:
    st.session_state.username = username
    # Reset answers if username changes
    reset_quiz()

# Show questions if username entered
if st.session_state.username:

    # Questions rendering with stable radio buttons
    for q_num, q_text in questions.items():
        opts = options[q_num]
        option_labels = list(opts.values())
        option_keys = list(opts.keys())

        current_answer_key = st.session_state.answers.get(q_num, None)
        if current_answer_key and current_answer_key in option_keys:
            default_index = option_keys.index(current_answer_key)
        else:
            default_index = 0

        selected_label = st.radio(
            q_text,
            option_labels,
            index=default_index,
            key=f"q{q_num}"
        )
        selected_key = option_keys[option_labels.index(selected_label)]
        st.session_state.answers[q_num] = selected_key

    # Submit button: only enabled if all questions answered
    if len(st.session_state.answers) == len(questions):
        if st.button("Submit Quiz"):
            st.session_state.submitted = True
    else:
        st.info("Please answer all questions to submit.")

    # Reset button
    if st.button("Reset Quiz"):
        reset_quiz()

    # Show results if submitted
    if st.session_state.submitted:
        personality, description = analyze_personality(st.session_state.answers)
        st.markdown(f"### Results for {st.session_state.username}")
        st.write(description)

else:
    st.info("Please enter your name to start the quiz.")
