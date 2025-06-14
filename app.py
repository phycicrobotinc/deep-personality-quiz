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

# ---------------------- GENERATE CERTIFICATE ----------------------
def generate_certificate(name, personality):
    width, height = 800, 400
    image = Image.new("RGB", (width, height), "white")
    draw = ImageDraw.Draw(image)

    # Load a font
    try:
        font_title = ImageFont.truetype("arial.ttf", 40)
        font_subtitle = ImageFont.truetype("arial.ttf", 24)
    except IOError:
        font_title = ImageFont.load_default()
        font_subtitle = ImageFont.load_default()

    # Draw title and subtitle
    draw.text((width // 2, 50), "Certificate of Personality", fill="navy", font=font_title, anchor="mm")
    draw.text((width // 2, 120), f"Presented to {name}", fill="black", font=font_subtitle, anchor="mm")
    draw.text((width // 2, 180), f"For your personality type:", fill="black", font=font_subtitle, anchor="mm")
    draw.text((width // 2, 240), f"{personality}", fill="darkgreen", font=font_title, anchor="mm")

    # Add some decoration lines
    draw.line([(50, 350), (width - 50, 350)], fill="navy", width=3)
    draw.line([(50, 355), (width - 50, 355)], fill="gold", width=3)

    # Save to bytes
    img_byte_arr = io.BytesIO()
    image.save(img_byte_arr, format='PNG')
    img_byte_arr.seek(0)
    return img_byte_arr

# ---------------------- STREAMLIT APP ----------------------
st.title("🧠 Deep Personality Quiz")

if not st.session_state.username or st.session_state.reset_requested:
    st.session_state.username = st.text_input("Enter your name to start:", value="")
    st.session_state.reset_requested = False
    if st.session_state.username:
        st.success(f"Welcome, {st.session_state.username}! You can start the quiz now.")
else:
    st.write(f"Welcome back, **{st.session_state.username}**!")

if st.session_state.username:
    # Render questions
    all_answered = True
    for q_num, q_text in questions.items():
        selected = st.session_state.answers.get(q_num, None)
        opts = options[q_num]
        try:
            answer = st.radio(q_text, list(opts.keys()), format_func=lambda x: opts[x], index=list(opts.keys()).index(selected) if selected else 0, key=f"q{q_num}")
        except ValueError:
            answer = st.radio(q_text, list(opts.keys()), format_func=lambda x: opts[x], index=0, key=f"q{q_num}")
        st.session_state.answers[q_num] = answer
        if not answer:
            all_answered = False

    # Submit button only if all questions answered
    if all_answered and not st.session_state.submitted:
        if st.button("Submit"):
            st.session_state.submitted = True
    elif not all_answered:
        st.warning("Please answer all questions before submitting.")

    # Reset button
    if st.button("Reset Test"):
        st.session_state.answers = {}
        st.session_state.submitted = False
        st.session_state.username = ""
        st.session_state.reset_requested = True

    # Show results if submitted
    if st.session_state.submitted:
        personality, description = analyze_personality(st.session_state.answers)
        st.markdown(f"### Results for {st.session_state.username}")
        st.write(description)

        cert_image = generate_certificate(st.session_state.username, personality)
        st.image(cert_image)
        st.download_button("Download Certificate", cert_image, file_name="certificate.png", mime="image/png")
