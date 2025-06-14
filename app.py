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
    "Q1": "What is your gender?",
    "Q2": "What is your age group?",
    "Q3": "What is your current employment status?",
    "Q4": "What is your approximate annual income?",
    "Q5": "What is your favorite way to spend weekends?",
    "Q6": "Red or Black?",
    "Q7": "Do you consider yourself more introverted or extroverted?",
    "Q8": "Do you enjoy trying new experiences?",
    "Q9": "Red or Black?",
    "Q10": "Are you more analytical or creative?",
    "Q11": "Do you prefer working alone or in a team?",
    "Q12": "Red or Black?",
    "Q13": "Are you more spontaneous or planned?",
    "Q14": "How often do you set long-term goals?",
    "Q15": "Red or Black?",
    "Q16": "Do you often reflect on your emotions?",
    "Q17": "How important is financial security to you?",
    "Q18": "Red or Black?",
    "Q19": "Do you make decisions quickly or after lots of thought?",
    "Q20": "What drives you most in life?"
}

options = {
    "Q1": {"A": "Male", "B": "Female", "C": "Other", "D": "Prefer not to say"},
    "Q2": {"A": "Under 18", "B": "18-24", "C": "25-34", "D": "35-44", "E": "45+"},
    "Q3": {"A": "Employed full-time", "B": "Part-time", "C": "Student", "D": "Unemployed", "E": "Retired"},
    "Q4": {"A": "<20k", "B": "20k-50k", "C": "50k-100k", "D": ">100k"},
    "Q5": {"A": "Reading/relaxing", "B": "Sports", "C": "Socializing", "D": "Creative hobbies"},
    "Q6": {"R": "Red", "B": "Black"},
    "Q7": {"A": "Introverted", "B": "Extroverted"},
    "Q8": {"A": "Love new experiences", "B": "Sometimes", "C": "Rarely"},
    "Q9": {"R": "Red", "B": "Black"},
    "Q10": {"A": "Analytical", "B": "Creative", "C": "Balanced"},
    "Q11": {"A": "Alone", "B": "Team"},
    "Q12": {"R": "Red", "B": "Black"},
    "Q13": {"A": "Spontaneous", "B": "Planned"},
    "Q14": {"A": "Often", "B": "Sometimes", "C": "Rarely"},
    "Q15": {"R": "Red", "B": "Black"},
    "Q16": {"A": "Yes", "B": "Sometimes", "C": "Not much"},
    "Q17": {"A": "Very", "B": "Somewhat", "C": "Not important"},
    "Q18": {"R": "Red", "B": "Black"},
    "Q19": {"A": "Quickly", "B": "After thought"},
    "Q20": {"A": "Success", "B": "Happiness", "C": "Growth", "D": "Peace"}
}

# ---------------------- ANALYZE PERSONALITY ----------------------
def analyze_personality(answers):
    red_count = sum(1 for q in questions if q in answers and answers[q] == "R")
    black_count = sum(1 for q in questions if q in answers and answers[q] == "B")

    traits = []
    if red_count > black_count:
        traits.append("bold")
    elif black_count > red_count:
        traits.append("calm")
    else:
        traits.append("balanced")

    if answers.get("Q7") == "A":
        traits.append("introspective")
    if answers.get("Q8") == "A":
        traits.append("curious")
    if answers.get("Q13") == "A":
        traits.append("spontaneous")
    if answers.get("Q14") == "A":
        traits.append("goal-oriented")

    if "bold" in traits and "curious" in traits:
        personality = "Explorer"
    elif "calm" in traits and "goal-oriented" in traits:
        personality = "Strategist"
    elif "spontaneous" in traits and "curious" in traits:
        personality = "Adventurer"
    else:
        personality = "Observer"

    return personality, f"You are a {personality}! This means you're {', '.join(traits)} and have a unique perspective on the world."

# ---------------------- CERTIFICATE IMAGE ----------------------
def generate_certificate(name, personality):
    width, height = 800, 400
    img = Image.new("RGB", (width, height), color="#fefefe")
    d = ImageDraw.Draw(img)

    try:
        title_font = ImageFont.truetype("arialbd.ttf", 48)
        name_font = ImageFont.truetype("arial.ttf", 36)
        personality_font = ImageFont.truetype("ariali.ttf", 30)
    except Exception:
        title_font = ImageFont.load_default()
        name_font = ImageFont.load_default()
        personality_font = ImageFont.load_default()

    border_color = "#2c3e50"
    border_thickness = 8
    for i in range(border_thickness):
        d.rectangle([i, i, width - i - 1, height - i - 1], outline=border_color)

    line_y = 100
    d.line([(50, line_y), (width - 50, line_y)], fill=border_color, width=3)

    title_text = "Certificate of Completion"
    w, h = d.textsize(title_text, font=title_font)
    d.text(((width - w) / 2, 30), title_text, fill=border_color, font=title_font)

    awarded_text = f"Awarded to: {name}"
    w, h = d.textsize(awarded_text, font=name_font)
    d.text(((width - w) / 2, line_y + 30), awarded_text, fill="#34495e", font=name_font)

    personality_text = f"Personality: {personality}"
    w, h = d.textsize(personality_text, font=personality_font)
    d.text(((width - w) / 2, line_y + 90), personality_text, fill="#34495e", font=personality_font)

    sig_line_y = height - 80
    d.line([(width / 2 - 150, sig_line_y), (width / 2 + 150, sig_line_y)], fill="#7f8c8d", width=2)
    sig_text = "Signature"
    w, h = d.textsize(sig_text, font=personality_font)
    d.text(((width - w) / 2, sig_line_y + 10), sig_text, fill="#7f8c8d", font=personality_font)

    buf = io.BytesIO()
    img.save(buf, format="PNG")
    buf.seek(0)
    return buf

# ---------------------- UI ----------------------

st.title("🧠 Deep Personality Quiz")

# Handle reset if requested
if st.session_state.reset_requested:
    st.session_state.submitted = False
    st.session_state.answers = {}
    st.session_state.username = ""
    st.session_state.reset_requested = False
    # No forced rerun, so user can continue interacting normally

if not st.session_state.submitted:
    username = st.text_input("Enter your name to begin:", value=st.session_state.username)
    if username:
        st.session_state.username = username

        for key in questions:
            if key not in st.session_state.answers:
                st.session_state.answers[key] = None

            answer = st.radio(questions[key], list(options[key].values()), index=-1, key=key)
            for k, v in options[key].items():
                if v == answer:
                    st.session_state.answers[key] = k

        if st.button("Submit"):
            if all(st.session_state.answers.values()):
                st.session_state.submitted = True
            else:
                st.warning("Please answer all questions.")

else:
    st.success(f"Thanks for completing the quiz, {st.session_state.username}!")
    personality, description = analyze_personality(st.session_state.answers)
    st.markdown(f"### Your Personality Type: {personality}")
    st.write(description)

    st.markdown("---")
    st.markdown("### Certificate of Completion")
    cert_buffer = generate_certificate(st.session_state.username, personality)
    st.image(cert_buffer, caption="Right-click to save your certificate.")

    if st.button("Retake Test"):
        # Mark reset requested, but don't force rerun
        st.session_state.reset_requested = True
        st.info("Quiz reset! You can start again when ready.")

