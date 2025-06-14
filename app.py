import streamlit as st
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO

# --------------------
# Profiles & Descriptions
# --------------------
reference_profiles = {
    "Thinker": {"Q1": "B", "Q2": "B", "Q3": "A", "Q4": "B", "Q5": "B", "Q6": "B", "Q7": "B", "Q8": "A", "Q9": "A", "Q10": "R", "Q11": "B", "Q12": "R", "Q13": "B", "Q14": "R", "Q15": "B"},
    "Adventurer": {"Q1": "C", "Q2": "C", "Q3": "C", "Q4": "C", "Q5": "C", "Q6": "C", "Q7": "C", "Q8": "C", "Q9": "C", "Q10": "B", "Q11": "R", "Q12": "B", "Q13": "R", "Q14": "B", "Q15": "R"},
    "Empath": {"Q1": "A", "Q2": "D", "Q3": "D", "Q4": "A", "Q5": "D", "Q6": "D", "Q7": "A", "Q8": "B", "Q9": "B", "Q10": "R", "Q11": "R", "Q12": "R", "Q13": "R", "Q14": "B", "Q15": "B"},
    "Innovator": {"Q1": "D", "Q2": "C", "Q3": "B", "Q4": "D", "Q5": "A", "Q6": "A", "Q7": "D", "Q8": "D", "Q9": "D", "Q10": "B", "Q11": "B", "Q12": "B", "Q13": "R", "Q14": "R", "Q15": "B"},
    "Leader": {"Q1": "B", "Q2": "A", "Q3": "D", "Q4": "D", "Q5": "A", "Q6": "A", "Q7": "D", "Q8": "D", "Q9": "D", "Q10": "B", "Q11": "B", "Q12": "R", "Q13": "B", "Q14": "R", "Q15": "B"},
    "Visionary": {"Q1": "D", "Q2": "C", "Q3": "B", "Q4": "B", "Q5": "C", "Q6": "D", "Q7": "C", "Q8": "B", "Q9": "B", "Q10": "R", "Q11": "R", "Q12": "B", "Q13": "B", "Q14": "R", "Q15": "R"},
    "Analyst": {"Q1": "B", "Q2": "B", "Q3": "A", "Q4": "B", "Q5": "A", "Q6": "B", "Q7": "B", "Q8": "A", "Q9": "A", "Q10": "B", "Q11": "B", "Q12": "R", "Q13": "B", "Q14": "B", "Q15": "B"},
    "Seeker": {"Q1": "C", "Q2": "C", "Q3": "C", "Q4": "C", "Q5": "C", "Q6": "C", "Q7": "A", "Q8": "C", "Q9": "C", "Q10": "R", "Q11": "R", "Q12": "R", "Q13": "R", "Q14": "R", "Q15": "R"},
}

profile_descriptions = {
    "Thinker": "🧠 You are methodical, rational, and logical. You think before acting and value clarity.",
    "Adventurer": "✈️ You thrive on spontaneity and exploration. Challenges excite you.",
    "Empath": "💖 You understand emotions deeply and connect well with others.",
    "Innovator": "💡 You love to create and solve problems in new ways.",
    "Leader": "🧭 You are confident, assertive, and naturally take charge.",
    "Visionary": "🌌 You dream big, think creatively, and pursue purpose.",
    "Analyst": "📊 You value precision, analysis, and strategic thinking.",
    "Seeker": "🌿 You are introspective, curious, and always searching for meaning."
}

# --------------------
# Questions & Options
# --------------------
questions = {
    "Q1": "How do you make decisions?",
    "Q2": "How do you handle failure?",
    "Q3": "Your ideal way to spend a weekend?",
    "Q4": "In a team, you're usually...",
    "Q5": "How do you approach risk?",
    "Q6": "Which best describes your thought process?",
    "Q7": "How do you react to conflict?",
    "Q8": "Which sounds more like you?",
    "Q9": "What’s your approach to goals?",
    "Q16": "What is your gender?",
    "Q17": "What is your age group?",
    "Q18": "How would you describe your financial status?",
    "Q10": "Red or Black?",
    "Q11": "Red or Black?",
    "Q12": "Red or Black?",
    "Q13": "Red or Black?",
    "Q14": "Red or Black?",
    "Q15": "Red or Black?",
}

options = {
    "Q1": {"A": "Emotional", "B": "Logical", "C": "Impulsive", "D": "Social"},
    "Q2": {"A": "Withdraw", "B": "Plan better", "C": "Try again", "D": "Talk it out"},
    "Q3": {"A": "Reading", "B": "Learning", "C": "Adventure", "D": "Party"},
    "Q4": {"A": "Organizer", "B": "Strategist", "C": "Wild card", "D": "Leader"},
    "Q5": {"A": "Calculated", "B": "Avoid", "C": "Thrill", "D": "Mood based"},
    "Q6": {"A": "Structured", "B": "Analytical", "C": "Flexible", "D": "Abstract"},
    "Q7": {"A": "Avoid", "B": "Negotiate", "C": "Challenge", "D": "Listen"},
    "Q8": {"A": "Planned", "B": "Emotional", "C": "Free", "D": "Driven"},
    "Q9": {"A": "Lists", "B": "Dream", "C": "Adapt", "D": "Visualize"},
    "Q16": {"A": "Male", "B": "Female", "C": "Other/Prefer not to say"},
    "Q17": {"A": "Under 18", "B": "18-30", "C": "31-50", "D": "Over 50"},
    "Q18": {"A": "Low", "B": "Moderate", "C": "High", "D": "Prefer not to say"},
    "Q10": {"R": "Red", "B": "Black"},
    "Q11": {"R": "Red", "B": "Black"},
    "Q12": {"R": "Red", "B": "Black"},
    "Q13": {"R": "Red", "B": "Black"},
    "Q14": {"R": "Red", "B": "Black"},
    "Q15": {"R": "Red", "B": "Black"},
}

# --------------------
# Helper Functions
# --------------------

def calculate_match(user_answers):
    scores = {}
    for profile, answers in reference_profiles.items():
        matches = sum(1 for q, ans in answers.items() if user_answers.get(q) == ans)
        scores[profile] = round(100 * matches / len(answers), 1)
    return scores

def get_top_profile(scores):
    return max(scores, key=scores.get)

def generate_certificate(name, personality, score):
    # Create image certificate
    width, height = 800, 400
    cert = Image.new("RGB", (width, height), "#f9f9f9")
    draw = ImageDraw.Draw(cert)
    font_path = None  # default font

    # Try to load a nicer font if available
    try:
        font_path = "arial.ttf"
        title_font = ImageFont.truetype(font_path, 40)
        subtitle_font = ImageFont.truetype(font_path, 28)
    except:
        title_font = ImageFont.load_default()
        subtitle_font = ImageFont.load_default()

    # Draw title bar
    draw.rectangle([(0,0), (width, 80)], fill="#3366cc")
    draw.text((20, 20), "🎓 Deep Personality Certificate", font=title_font, fill="white")

    # Draw name
    draw.text((50, 120), f"Name: {name}", font=subtitle_font, fill="black")

    # Draw personality and emoji
    emoji = profile_descriptions[personality].split()[0]
    draw.text((50, 170), f"Personality: {personality} {emoji}", font=subtitle_font, fill="black")

    # Draw match score
    draw.text((50, 220), f"Match: {score}%", font=subtitle_font, fill="black")

    # Description
    desc = profile_descriptions.get(personality, "")
    draw.multiline_text((50, 270), desc, font=subtitle_font, fill="black")

    return cert

# --------------------
# Streamlit App
# --------------------

st.set_page_config(page_title="Deep Personality Quiz", layout="centered")
st.title("🌟 Deep Personality Quiz")

if "answers" not in st.session_state:
    st.session_state.answers = {}

if "submitted" not in st.session_state:
    st.session_state.submitted = False

# User name input
if not st.session_state.submitted:
    username = st.text_input("Please enter your name:", key="username")
else:
    username = st.session_state.username

if not st.session_state.submitted:
    if username:
        st.session_state.username = username

        st.header("Answer the following questions:")

        # Display questions except the red/black ones first
        for qid in ["Q1","Q2","Q3","Q4","Q5","Q6","Q7","Q8","Q9","Q16","Q17","Q18"]:
            st.write(f"**{questions[qid]}**")
            choice = st.radio("", options=[f"{k}: {v}" for k,v in options[qid].items()], key=qid)
            ans = choice.split(":")[0]  # letter code
            st.session_state.answers[qid] = ans

        # Then the last 6 red or black questions
        st.subheader("Final 6 Questions: Red or Black?")
        for qid in ["Q10","Q11","Q12","Q13","Q14","Q15"]:
            st.write(f"**{questions[qid]}**")
            choice = st.radio("", options=[f"{k}: {v}" for k,v in options[qid].items()], key=qid)
            ans = choice.split(":")[0]
            st.session_state.answers[qid] = ans

        if st.button("Submit Quiz"):
            st.session_state.submitted = True
else:
    st.header(f"Thank you, {st.session_state.username}!")
    scores = calculate_match(st.session_state.answers)
    top_profile = get_top_profile(scores)
    top_score = scores[top_profile]
    st.success(f"Your dominant personality type is **{top_profile}** with a match of **{top_score}%**.")
    st.write(profile_descriptions[top_profile])

    # Show all scores
    st.write("### Your match scores with all personality types:")
    for p, s in sorted(scores.items(), key=lambda x: x[1], reverse=True):
        st.write(f"- **{p}**: {s}%")

    # Generate and show certificate
    cert_img = generate_certificate(st.session_state.username, top_profile, top_score)
    buf = BytesIO()
    cert_img.save(buf, format="PNG")
    byte_im = buf.getvalue()

    st.image(cert_img, caption="Your Personality Certificate")
    st.download_button(
        label="Download Certificate as PNG",
        data=byte_im,
        file_name=f"{st.session_state.username}_personality_certificate.png",
        mime="image/png"
    )

    if st.button("Retake Quiz"):
        st.session_state.submitted = False
        st.session_state.answers = {}
        st.experimental_rerun()
