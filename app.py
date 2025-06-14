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

# ---------------------- QUESTIONS & OPTIONS ----------------------
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

# ---------------------- CERTIFICATE GENERATOR ----------------------
def generate_certificate(username, personality):
    width, height = 800, 600
    cert = Image.new("RGB", (width, height), color=(255, 255, 255))
    draw = ImageDraw.Draw(cert)

    try:
        title_font = ImageFont.truetype("arial.ttf", 40)
        text_font = ImageFont.truetype("arial.ttf", 24)
    except IOError:
        title_font = text_font = ImageFont.load_default()

    draw.text((width // 2 - 180, 80), "Deep Personality Quiz", font=title_font, fill="black")
    draw.text((width // 2 - 150, 200), f"Congratulations, {username}!", font=text_font, fill="black")
    draw.text((width // 2 - 200, 300), f"Your personality type is: {personality}", font=text_font, fill="black")

    buffer = io.BytesIO()
    cert.save(buffer, format="PNG")
    buffer.seek(0)
    return buffer

# ---------------------- STREAMLIT UI ----------------------
st.title("🧠 Deep Personality Quiz")

# Reset if requested
if st.session_state.reset_requested:
    st.session_state.answers = {}
    st.session_state.submitted = False
    st.session_state.username = ""
    st.session_state.reset_requested = False
    st.experimental_rerun()

# Get user name
if not st.session_state.username:
    st.session_state.username = st.text_input("Enter your name to begin:")

# Show the quiz if username entered
if st.session_state.username:
    for q_num, q_text in questions.items():
        if q_num not in st.session_state.answers:
            st.session_state.answers[q_num] = None
        st.session_state.answers[q_num] = st.radio(
            q_text,
            list(options[q_num].values()),
            index=-1,
            key=f"q{q_num}"
        )

    all_answered = all(st.session_state.answers[q] is not None for q in questions)

    if st.button("Finish Quiz") and all_answered:
        st.session_state.submitted = True

    if not all_answered:
        st.warning("Please answer all the questions before submitting.")

# ---------------------- SHOW RESULTS ----------------------
if st.session_state.submitted:
    reverse_answers = {}
    for q, answer in st.session_state.answers.items():
        for key, val in options[q].items():
            if val == answer:
                reverse_answers[q] = key

    personality, description = analyze_personality(reverse_answers)
    st.success(description)

    cert = generate_certificate(st.session_state.username, personality)
    st.image(cert, caption="Your Certificate", use_column_width=True)

    st.download_button(
        label="Download Your Certificate",
        data=cert,
        file_name=f"{st.session_state.username}_certificate.png",
        mime="image/png"
    )

    if st.button("Retake Test"):
        st.session_state.reset_requested = True
        st.experimental_rerun()
