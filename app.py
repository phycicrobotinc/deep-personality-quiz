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

# ---------------------- CERTIFICATE GENERATION ----------------------
def generate_certificate(name, personality, description):
    # Create blank image
    width, height = 800, 600
    image = Image.new("RGB", (width, height), color="#f5f5dc")  # light beige background
    draw = ImageDraw.Draw(image)

    # Load fonts (use default PIL font or replace with .ttf path if available)
    try:
        title_font = ImageFont.truetype("arial.ttf", 40)
        subtitle_font = ImageFont.truetype("arial.ttf", 30)
        body_font = ImageFont.truetype("arial.ttf", 20)
    except IOError:
        title_font = ImageFont.load_default()
        subtitle_font = ImageFont.load_default()
        body_font = ImageFont.load_default()

    # Draw border
    border_color = "#6a0dad"  # purple
    border_width = 10
    draw.rectangle([border_width//2, border_width//2, width-border_width//2, height-border_width//2], outline=border_color, width=border_width)

    # Title
    draw.text((width//2, 60), "Personality Certificate", fill=border_color, font=title_font, anchor="mm")

    # Name
    draw.text((width//2, 150), name, fill="#333333", font=subtitle_font, anchor="mm")

    # Personality Type
    draw.text((width//2, 210), f"Personality: {personality}", fill="#555555", font=subtitle_font, anchor="mm")

    # Description (wrap text)
    import textwrap
    lines = textwrap.wrap(description, width=50)
    y_text = 270
    for line in lines:
        draw.text((width//2, y_text), line, fill="#444444", font=body_font, anchor="mm")
        y_text += 30

    return image

# ---------------------- APP UI ----------------------
st.set_page_config(page_title="🧠 Deep Personality Quiz", layout="centered")

st.title("🧠 Deep Personality Quiz")
st.write("Fill out all questions below and get your personality result!")

# Reset button
if st.button("Reset Quiz"):
    st.session_state.submitted = False
    st.session_state.answers = {}
    st.session_state.username = ""

# Enter username
if not st.session_state.submitted:
    name = st.text_input("Enter your name:", value=st.session_state.username)
    if name != st.session_state.username:
        st.session_state.username = name
        st.session_state.answers = {}  # clear answers if username changed

    if not st.session_state.username.strip():
        st.warning("Please enter your name to start the quiz.")
        st.stop()

# Questions (only show if not submitted)
if not st.session_state.submitted:
    for q_num in sorted(questions.keys()):
        q_text = questions[q_num]
        opts = options[q_num]

        # Prepare options list for selectbox with placeholder
        option_keys = list(opts.keys())
        option_labels = [f"{key}: {opts[key]}" for key in option_keys]
        placeholder = "Choose an option"
        select_options = [placeholder] + option_labels

        # Get current answer if any
        current_answer = st.session_state.answers.get(q_num, None)
        if current_answer in option_keys:
            default_index = option_keys.index(current_answer) + 1
        else:
            default_index = 0  # placeholder

        selected_label = st.selectbox(
            label=q_text,
            options=select_options,
            index=default_index,
            key=f"q{q_num}"
        )

        # Update session state only if a real option is selected
        if selected_label != placeholder:
            selected_key = selected_label.split(":")[0]
            st.session_state.answers[q_num] = selected_key
        else:
            # If placeholder selected, remove answer if any
            st.session_state.answers.pop(q_num, None)

    # Check if all questions answered
    if len(st.session_state.answers) < len(questions):
        st.warning("Please answer all questions to submit.")
    else:
        if st.button("Submit Quiz"):
            st.session_state.submitted = True

# Show results and certificate
if st.session_state.submitted:
    personality, description = analyze_personality(st.session_state.answers)

    st.header("Your Personality Result")
    st.markdown(f"### {personality}")
    st.write(description)

    cert_img = generate_certificate(st.session_state.username, personality, description)

    st.image(cert_img, caption="Your Personality Certificate", use_column_width=True)

    # Prepare certificate download
    buf = io.BytesIO()
    cert_img.save(buf, format="PNG")
    byte_im = buf.getvalue()

    st.download_button(
        label="Download Certificate",
        data=byte_im,
        file_name=f"{st.session_state.username}_personality_certificate.png",
        mime="image/png"
    )
pip install gspread oauth2client
