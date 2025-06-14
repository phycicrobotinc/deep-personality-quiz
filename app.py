import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import io
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# ---------------------- GOOGLE SHEETS SETUP ----------------------
def connect_to_google_sheet():
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name("your_service_account.json", scope)
    client = gspread.authorize(creds)
    sheet = client.open("PersonalityQuizData").sheet1  # Change this to your sheet name
    return sheet

def log_to_sheet(username, personality, answers):
    try:
        sheet = connect_to_google_sheet()
        row = [username, personality] + [answers.get(q, "") for q in range(1, 21)]
        sheet.append_row(row)
    except Exception as e:
        st.error(f"Error logging to Google Sheets: {e}")

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
def generate_certificate(username, personality):
    width, height = 700, 400
    image = Image.new("RGB", (width, height), color="#f8f4e3")
    draw = ImageDraw.Draw(image)

    # Fonts (adjust path if needed)
    try:
        title_font = ImageFont.truetype("arial.ttf", 40)
        subtitle_font = ImageFont.truetype("arial.ttf", 24)
    except IOError:
        title_font = ImageFont.load_default()
        subtitle_font = ImageFont.load_default()

    draw.text((width//2, 50), "Certificate of Personality", font=title_font, fill="#4b3b2b", anchor="mm")
    draw.text((width//2, 130), f"This certifies that", font=subtitle_font, fill="#4b3b2b", anchor="mm")
    draw.text((width//2, 180), username, font=title_font, fill="#a0522d", anchor="mm")
    draw.text((width//2, 240), f"is identified as a", font=subtitle_font, fill="#4b3b2b", anchor="mm")
    draw.text((width//2, 290), personality, font=title_font, fill="#d2691e", anchor="mm")
    draw.text((width//2, 350), "Deep Personality Quiz 2025", font=subtitle_font, fill="#4b3b2b", anchor="mm")

    # Draw border
    border_color = "#d2691e"
    draw.rectangle([(10, 10), (width-10, height-10)], outline=border_color, width=5)

    # Save to bytes
    buffer = io.BytesIO()
    image.save(buffer, format="PNG")
    buffer.seek(0)
    return buffer

# ---------------------- STREAMLIT UI ----------------------

st.set_page_config(page_title="🧠 Deep Personality Quiz", layout="centered")

st.title("🧠 Deep Personality Quiz")

if not st.session_state.username:
    username_input = st.text_input("Enter your name to start:", value="")
    if username_input:
        st.session_state.username = username_input
        st.experimental_rerun()
    else:
        st.stop()

if not st.session_state.submitted:
    st.header(f"Hello, {st.session_state.username}! Please answer the following questions:")

    all_answered = True
    for q_num, q_text in questions.items():
        opts = options[q_num]
        current_answer = st.session_state.answers.get(q_num, None)
        choice = st.radio(q_text, options=list(opts.keys()), format_func=lambda x: opts[x], index=list(opts.keys()).index(current_answer) if current_answer else 0, key=f"q{q_num}")
        st.session_state.answers[q_num] = choice

        # Check if answer is selected properly
        if st.session_state.answers[q_num] not in opts:
            all_answered = False

    if not all_answered:
        st.warning("Please answer all questions to proceed.")
    else:
        if st.button("Submit Quiz"):
            st.session_state.submitted = True

if st.session_state.submitted:
    personality, description = analyze_personality(st.session_state.answers)
    st.success(description)

    cert_image_buffer = generate_certificate(st.session_state.username, personality)
    st.image(cert_image_buffer)

    st.download_button("Download Certificate", cert_image_buffer, file_name="personality_certificate.png", mime="image/png")

    # Log the results to Google Sheets
    log_to_sheet(st.session_state.username, personality, st.session_state.answers)

    if st.button("Retake Quiz"):
        st.session_state.submitted = False
        st.session_state.answers = {}
        st.session_state.username = ""
        st.experimental_rerun()
