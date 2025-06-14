import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import io
import datetime

# ----------- STATE INIT -----------
if "submitted" not in st.session_state:
    st.session_state.submitted = False
if "answers" not in st.session_state:
    st.session_state.answers = {}
if "username" not in st.session_state:
    st.session_state.username = ""
if "reset_requested" not in st.session_state:
    st.session_state.reset_requested = False

# ----------- QUESTIONS & OPTIONS -----------
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

# ----------- ANALYZE PERSONALITY -----------
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

# ----------- CERTIFICATE GENERATION -----------
def generate_certificate(username, personality):
    width, height = 700, 400
    image = Image.new("RGB", (width, height), color="#1F2937")  # Dark background
    draw = ImageDraw.Draw(image)

    # Load a TTF font file, fallback to default if not available
    try:
        font_title = ImageFont.truetype("arial.ttf", 40)
        font_subtitle = ImageFont.truetype("arial.ttf", 24)
        font_text = ImageFont.truetype("arial.ttf", 20)
    except:
        font_title = ImageFont.load_default()
        font_subtitle = ImageFont.load_default()
        font_text = ImageFont.load_default()

    # Decorative border
    border_color = "#F59E0B"  # Amber color
    border_thickness = 8
    for i in range(border_thickness):
        draw.rectangle([i, i, width - i - 1, height - i - 1], outline=border_color)

    # Title
    draw.text((width // 2, 50), "Certificate of Completion", font=font_title, fill="#FBBF24", anchor="mm")
    # Subtitle
    draw.text((width // 2, 120), f"Awarded to {username}", font=font_subtitle, fill="white", anchor="mm")
    # Personality
    draw.text((width // 2, 180), f"For your personality type:", font=font_text, fill="white", anchor="mm")
    draw.text((width // 2, 220), f"{personality}", font=font_subtitle, fill="#F59E0B", anchor="mm")

    # Date
    date_str = datetime.datetime.now().strftime("%B %d, %Y")
    draw.text((width // 2, 350), f"Issued on {date_str}", font=font_text, fill="white", anchor="mm")

    # Return image bytes
    buf = io.BytesIO()
    image.save(buf, format="PNG")
    buf.seek(0)
    return buf

# ----------- APP UI -----------
def reset_quiz():
    st.session_state.username = ""
    st.session_state.answers = {}
    st.session_state.submitted = False

st.title("🧠 Deep Personality Quiz")

if st.session_state.username == "":
    username_input = st.text_input("Enter your name to start the quiz:", key="username_input")
    if username_input:
        st.session_state.username = username_input
        st.experimental_rerun()
else:
    st.write(f"Hello, **{st.session_state.username}**! Please answer all questions below.")

    # Display questions with radio options, no prefill by default
    for q_num in range(1, len(questions) + 1):
        q_text = questions[q_num]
        opts = options[q_num]

        # Get current answer or None if not answered
        current_answer = st.session_state.answers.get(q_num)

        # Radio button with no default selected if unanswered
        answer = st.radio(
            q_text,
            list(opts.keys()),
            format_func=lambda x: opts[x],
            index=list(opts.keys()).index(current_answer) if current_answer in opts else None,
            key=f"q{q_num}"
        )

        # Update the session state answers
        st.session_state.answers[q_num] = answer

    # Check all questions answered:
    all_answered = all(q in st.session_state.answers for q in questions)

    if not all_answered:
        st.warning("Please answer all questions before submitting.")
    else:
        if st.button("Submit Quiz"):
            st.session_state.submitted = True

    if st.session_state.submitted:
        personality, description = analyze_personality(st.session_state.answers)
        st.success(description)

        cert_image = generate_certificate(st.session_state.username, personality)
        st.image(cert_image, caption="Your Certificate", use_column_width=True)
        st.download_button("Download Certificate", cert_image, file_name="certificate.png", mime="image/png")

        if st.button("Restart Quiz"):
            reset_quiz()
            st.experimental_rerun()
