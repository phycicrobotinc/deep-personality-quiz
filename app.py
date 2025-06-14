pip install gspread
import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import io
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime

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

# ---------------------- GOOGLE SHEETS SETUP ----------------------
SERVICE_ACCOUNT_FILE = 'path/to/your/service-account-key.json'  # <- change this!

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
creds = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
gc = gspread.authorize(creds)
sheet = gc.open("phycic robot 1").sheet1  # your Google Sheet name here

def log_quiz_results(username, answers):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    ordered_answers = [answers.get(i, "") for i in range(1, 21)]
    row = [timestamp, username] + ordered_answers
    sheet.append_row(row)

# ---------------------- CERTIFICATE GENERATION ----------------------
def generate_certificate(name, personality):
    width, height = 800, 400
    img = Image.new('RGB', (width, height), color='navy')
    draw = ImageDraw.Draw(img)

    # Load a font (using default PIL font here for portability)
    try:
        font_title = ImageFont.truetype("arial.ttf", 50)
        font_body = ImageFont.truetype("arial.ttf", 30)
    except IOError:
        font_title = ImageFont.load_default()
        font_body = ImageFont.load_default()

    # Draw text
    draw.text((width//2 - 180, 50), "Certificate of Completion", fill="white", font=font_title)
    draw.text((width//2 - 230, 150), f"Presented to: {name}", fill="white", font=font_body)
    draw.text((width//2 - 230, 220), f"Personality Type: {personality}", fill="white", font=font_body)
    draw.text((width//2 - 350, 290), "Thank you for completing the Deep Personality Quiz!", fill="white", font=font_body)

    # Save to bytes
    buf = io.BytesIO()
    img.save(buf, format='PNG')
    buf.seek(0)
    return buf

# ---------------------- MAIN APP ----------------------
def main():
    st.title("🧠 Deep Personality Quiz")

    # Username input (reset answers if username changes)
    username = st.text_input("Enter your name to start the quiz:", value=st.session_state.username)
    if username != st.session_state.username:
        st.session_state.username = username
        st.session_state.answers = {}
        st.session_state.submitted = False

    if not username:
        st.warning("Please enter your name to proceed.")
        return

    # Show questions if not submitted
    if not st.session_state.submitted:
        for q_num in range(1, 21):
            q_text = questions[q_num]
            opts = options[q_num]
            # Pre-select previously chosen answer if any
            default_answer = st.session_state.answers.get(q_num, None)
            st.session_state.answers[q_num] = st.radio(
                q_text,
                options=[f"{key}: {val}" for key, val in opts.items()],
                index=list(opts.keys()).index(default_answer) if default_answer in opts else 0,
                key=f"q{q_num}"
            )

        # Check if all questions are answered before allowing submit
        if all(st.session_state.answers.get(i) for i in range(1, 21)):
            if st.button("Submit"):
                # Extract just the letter key (before colon) from the selected option string
                for i in range(1, 21):
                    st.session_state.answers[i] = st.session_state.answers[i].split(":")[0]
                st.session_state.submitted = True
        else:
            st.info("Please answer all questions before submitting.")

    # After submit - show results and certificate
    if st.session_state.submitted:
        personality, description = analyze_personality(st.session_state.answers)
        st.header(f"Hello {st.session_state.username}, your personality is: {personality}")
        st.write(description)

        # Log to Google Sheets once
        if not st.session_state.get("logged_to_sheet", False):
            try:
                log_quiz_results(st.session_state.username, st.session_state.answers)
                st.session_state.logged_to_sheet = True
                st.success("Your results have been logged successfully!")
            except Exception as e:
                st.error(f"Failed to log results: {e}")

        # Generate and show certificate
        cert_image = generate_certificate(st.session_state.username, personality)
        st.image(cert_image)

        # Provide download button for the certificate
        st.download_button("Download Certificate", cert_image, file_name="certificate.png", mime="image/png")

    # Reset button to start over
    if st.button("Reset Quiz"):
        st.session_state.submitted = False
        st.session_state.answers = {}
        st.session_state.username = ""
        st.session_state.logged_to_sheet = False
        st.experimental_rerun()

if __name__ == "__main__":
    main()
