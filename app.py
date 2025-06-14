import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import io

# ------------- INIT STATE -----------------
if "submitted" not in st.session_state:
    st.session_state.submitted = False
if "answers" not in st.session_state:
    st.session_state.answers = {}
if "username" not in st.session_state:
    st.session_state.username = ""

# ------------- QUESTIONS -----------------
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

# ------------- PERSONALITY ANALYSIS -------------
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

    description = (
        f"You are a {personality}! This means you're "
        + ", ".join(traits)
        + " and have a unique perspective on the world."
    )
    return personality, description

# ------------- CERTIFICATE GENERATION -------------
def generate_certificate(name, personality):
    img = Image.new("RGB", (600, 300), color="white")
    d = ImageDraw.Draw(img)
    try:
        font = ImageFont.truetype("arial.ttf", 24)
    except Exception:
        font = ImageFont.load_default()

    d.text((30, 50), "Certificate of Completion", fill="black", font=font)
    d.text((30, 120), f"Awarded to: {name}", fill="black", font=font)
    d.text((30, 170), f"Personality: {personality}", fill="black", font=font)

    buf = io.BytesIO()
    img.save(buf, format="PNG")
    buf.seek(0)
    return buf

# ------------- UI -------------
st.title("🧠 Deep Personality Quiz")

if not st.session_state.submitted:
    username = st.text_input("Enter your name to begin:", value=st.session_state.username)
    if username:
        st.session_state.username = username

        # Initialize unanswered questions
        for key in questions:
            if key not in st.session_state.answers:
                st.session_state.answers[key] = None

        # Show questions with radio buttons for answers
        for key in questions:
            selected_option = st.session_state.answers.get(key)

            # Get list of option texts
            option_texts = list(options[key].values())

            # Figure out index of selected option or -1 if None
            if selected_option:
                # Find the option key (e.g. "A") to get text
                current_text = options[key].get(selected_option)
                index = option_texts.index(current_text) if current_text in option_texts else 0
            else:
                index = 0  # default to first option to avoid -1 errors

            answer = st.radio(questions[key], option_texts, index=index, key=key)

            # Update session state answer key with option code ("A", "B", "R", etc)
            for code, text in options[key].items():
                if text == answer:
                    st.session_state.answers[key] = code
                    break

        if st.button("Submit"):
            # Check all questions answered (no None)
            if None in st.session_state.answers.values():
                st.warning("Please answer all questions.")
            else:
                st.session_state.submitted = True

else:
    st.success(f"Thanks for completing the quiz, {st.session_state.username}!")

    personality, description = analyze_personality(st.session_state.answers)

    st.markdown(f"### Your Personality Type: {personality}")
    st.write(description)

    st.markdown("---")
    st.markdown("### Certificate of Completion")
    certificate_img = generate_certificate(st.session_state.username, personality)
    st.image(certificate_img, caption="Right-click or tap and hold to save your certificate.")

