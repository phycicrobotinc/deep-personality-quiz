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

    description = f"You are a {personality}! This means you're {', '.join(traits)} and have a unique perspective on the world."
    return personality, description

# ---------------------- CERTIFICATE GENERATION ----------------------
def generate_certificate(username, personality, description):
    width, height = 800, 400
    background_color = (255, 255, 204)  # light yellow
    img = Image.new('RGB', (width, height), color=background_color)
    draw = ImageDraw.Draw(img)

    # Fonts (use built-in or system fonts if available)
    try:
        title_font = ImageFont.truetype("arial.ttf", 40)
        body_font = ImageFont.truetype("arial.ttf", 24)
    except IOError:
        title_font = ImageFont.load_default()
        body_font = ImageFont.load_default()

    # Draw Title
    title_text = "Personality Quiz Certificate"
    w, h = draw.textsize(title_text, font=title_font)
    draw.text(((width - w) / 2, 40), title_text, fill="darkblue", font=title_font)

    # Draw Username
    name_text = f"Presented to: {username or 'Anonymous'}"
    w, h = draw.textsize(name_text, font=body_font)
    draw.text(((width - w) / 2, 120), name_text, fill="black", font=body_font)

    # Draw Personality
    pers_text = f"Personality Type: {personality}"
    w, h = draw.textsize(pers_text, font=body_font)
    draw.text(((width - w) / 2, 170), pers_text, fill="darkgreen", font=body_font)

    # Draw Description (wrapped text)
    margin = 40
    current_h = 220
    line_height = 28
    desc_lines = []
    words = description.split()
    line = ""
    for word in words:
        if draw.textsize(line + word, font=body_font)[0] < width - 2 * margin:
            line += word + " "
        else:
            desc_lines.append(line)
            line = word + " "
    desc_lines.append(line)

    for line in desc_lines:
        draw.text((margin, current_h), line, fill="black", font=body_font)
        current_h += line_height

    # Save to bytes buffer
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    buf.seek(0)
    return buf

# ---------------------- APP UI ----------------------
st.title("🎯 Deep Personality Quiz")

# Reset quiz on button click
def reset_quiz():
    st.session_state.submitted = False
    st.session_state.answers = {}
    st.session_state.username = ""
    st.session_state.reset_requested = True

# Username input (optional)
if not st.session_state.submitted:
    st.session_state.username = st.text_input("Enter your name (optional):", value=st.session_state.username)

# Questions form
if not st.session_state.submitted:
    with st.form("quiz_form"):
        for q_id, question in questions.items():
            opts = options[q_id]
            # Show radio buttons, prefill none
            st.session_state.answers[q_id] = st.radio(
                question,
                list(opts.keys()),
                format_func=lambda x: opts[x],
                index=0 if q_id not in st.session_state.answers else list(opts.keys()).index(st.session_state.answers.get(q_id, list(opts.keys())[0])),
                key=q_id,
                horizontal=True
            )
        submitted = st.form_submit_button("Finish Quiz")

        if submitted:
            # Check all questions answered
            if len(st.session_state.answers) < len(questions) or any(a is None for a in st.session_state.answers.values()):
                st.warning("Please answer all questions before submitting.")
            else:
                st.session_state.submitted = True

if st.session_state.submitted:
    # Analyze personality
    personality, description = analyze_personality(st.session_state.answers)

    st.header(f"Hello, {st.session_state.username or 'Participant'}!")
    st.subheader("Your Personality Result:")
    st.markdown(f"**{personality}**")
    st.write(description)

    # Generate and show certificate
    cert_img = generate_certificate(st.session_state.username, personality, description)
    st.image(cert_img)

    # Download certificate button
    st.download_button(
        label="Download your Certificate",
        data=cert_img,
        file_name="personality_certificate.png",
        mime="image/png"
    )

    # Retake button
    if st.button("Retake Quiz"):
        reset_quiz()
        st.experimental_rerun()

# Prevent auto-fill on rerun by clearing answers if reset requested
if st.session_state.reset_requested:
    for q in questions:
        st.session_state.answers[q] = None
    st.session_state.reset_requested = False
