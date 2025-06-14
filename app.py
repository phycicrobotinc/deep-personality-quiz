# ---------------------- CERTIFICATE ----------------------
def generate_certificate(name, personality):
    width, height = 800, 600
    image = Image.new("RGB", (width, height), color=(30, 30, 30))
    draw = ImageDraw.Draw(image)

    try:
        font_large = ImageFont.truetype("arial.ttf", 48)
        font_small = ImageFont.truetype("arial.ttf", 28)
    except:
        font_large = ImageFont.load_default()
        font_small = ImageFont.load_default()

    draw.rectangle([(50, 50), (750, 550)], outline="gold", width=6)
    draw.text((width//2 - 200, 100), "🎖️ Certificate of Personality", font=font_large, fill="white")
    draw.text((width//2 - 180, 250), f"Awarded to:", font=font_small, fill="lightgray")
    draw.text((width//2 - 150, 300), name, font=font_large, fill="cyan")
    draw.text((width//2 - 250, 400), f"For being a true {personality}!", font=font_small, fill="gold")

    byte_io = io.BytesIO()
    image.save(byte_io, format="PNG")
    byte_io.seek(0)
    return byte_io

# ---------------------- RESULTS ----------------------
def show_results():
    personality, description = analyze_personality(st.session_state.answers)

    st.subheader("🎯 Your Personality Result")
    st.success(description)

    cert_image = generate_certificate(st.session_state.username, personality)
    st.image(cert_image, caption="Your Certificate", use_column_width=True)
    st.download_button("📥 Download Certificate", cert_image, file_name="personality_certificate.png")

    if st.button("🔁 Retake Quiz"):
        st.session_state.reset_requested = True
        st.session_state.submitted = False
        st.session_state.answers = {}
        st.experimental_rerun()

# ---------------------- MAIN ----------------------
def main():
    if st.session_state.submitted:
        show_results()
    else:
        show_quiz()

if __name__ == "__main__":
    main()
import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import io
import gspread
from google.oauth2.service_account import Credentials

# ---------------------- GOOGLE SHEETS SETUP ----------------------
SHEET_NAME = "phycic robot 1"
SCOPE = ["https://www.googleapis.com/auth/spreadsheets"]
CREDS = Credentials.from_service_account_file("service_account.json", scopes=SCOPE)
client = gspread.authorize(CREDS)
sheet = client.open(SHEET_NAME).sheet1

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
# ---------------------- QUIZ FORM ----------------------
def show_quiz():
    st.title("🧠 Deep Personality Quiz")

    if st.session_state.reset_requested or not st.session_state.username:
        st.session_state.username = st.text_input("Enter your name to begin:")
        if st.session_state.username:
            st.session_state.reset_requested = False
            st.session_state.answers = {}
        return

    with st.form("quiz_form"):
        for q_num, q_text in questions.items():
            opts = options[q_num]
            selected = st.radio(
                f"{q_num}. {q_text}",
                list(opts.values()),
                index=None,
                key=f"q{q_num}"
            )

            # Save answer in reverse (value to key)
            if selected:
                reverse_lookup = {v: k for k, v in opts.items()}
                st.session_state.answers[q_num] = reverse_lookup[selected]

        submitted = st.form_submit_button("Submit Quiz")
        if submitted:
            unanswered = [q for q in questions if q not in st.session_state.answers]
            if unanswered:
                st.warning(f"Please answer all questions before submitting. Unanswered: {unanswered}")
            else:
                st.session_state.submitted = True
                update_google_sheet(st.session_state.username, st.session_state.answers)

# ---------------------- GOOGLE SHEETS LOGGING ----------------------
def update_google_sheet(username, answers):
    try:
        import gspread
        from google.oauth2.service_account import Credentials

        scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        creds = Credentials.from_service_account_file("service_account.json", scopes=scope)
        client = gspread.authorize(creds)
        sheet = client.open("phycic robot 1").sheet1

        row = [username] + [answers.get(q, "") for q in sorted(questions.keys())]
        sheet.append_row(row)
    except Exception as e:
        st.error(f"Error saving to Google Sheets: {e}")
