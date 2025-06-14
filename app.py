import streamlit as st
import json, random, os
from PIL import Image, ImageDraw, ImageFont

# == FILE PATH ==
PROFILES_FILE = "deep_profiles.json"

# == PERSONALITY PROFILES ==
reference_profiles = {
    "Thinker":     {"Q1": "B", "Q2": "B", "Q3": "A", "Q4": "B", "Q5": "B", "Q6": "B", "Q7": "B", "Q8": "A", "Q9": "A", "Q10": "R", "Q11": "B", "Q12": "R", "Q13": "B", "Q14": "R", "Q15": "B"},
    "Adventurer": {"Q1": "C", "Q2": "C", "Q3": "C", "Q4": "C", "Q5": "C", "Q6": "C", "Q7": "C", "Q8": "C", "Q9": "C", "Q10": "B", "Q11": "R", "Q12": "B", "Q13": "R", "Q14": "B", "Q15": "R"},
    "Empath":     {"Q1": "A", "Q2": "D", "Q3": "D", "Q4": "A", "Q5": "D", "Q6": "D", "Q7": "A", "Q8": "B", "Q9": "B", "Q10": "R", "Q11": "R", "Q12": "R", "Q13": "R", "Q14": "B", "Q15": "B"},
    "Innovator":  {"Q1": "D", "Q2": "C", "Q3": "B", "Q4": "D", "Q5": "A", "Q6": "A", "Q7": "D", "Q8": "D", "Q9": "D", "Q10": "B", "Q11": "B", "Q12": "B", "Q13": "R", "Q14": "R", "Q15": "B"},
    "Leader":     {"Q1": "B", "Q2": "A", "Q3": "D", "Q4": "D", "Q5": "A", "Q6": "A", "Q7": "D", "Q8": "D", "Q9": "D", "Q10": "B", "Q11": "B", "Q12": "R", "Q13": "B", "Q14": "R", "Q15": "B"},
    "Visionary":  {"Q1": "D", "Q2": "C", "Q3": "B", "Q4": "B", "Q5": "C", "Q6": "D", "Q7": "C", "Q8": "B", "Q9": "B", "Q10": "R", "Q11": "R", "Q12": "B", "Q13": "B", "Q14": "R", "Q15": "R"},
    "Analyst":    {"Q1": "B", "Q2": "B", "Q3": "A", "Q4": "B", "Q5": "A", "Q6": "B", "Q7": "B", "Q8": "A", "Q9": "A", "Q10": "B", "Q11": "B", "Q12": "R", "Q13": "B", "Q14": "B", "Q15": "B"},
    "Seeker":     {"Q1": "C", "Q2": "C", "Q3": "C", "Q4": "C", "Q5": "C", "Q6": "C", "Q7": "A", "Q8": "C", "Q9": "C", "Q10": "R", "Q11": "R", "Q12": "R", "Q13": "R", "Q14": "R", "Q15": "R"},
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

# == QUESTIONS & OPTIONS ==
questions = {
    "Q1":"How do you make decisions?",
    "Q2":"How do you handle failure?",
    "Q3":"Your ideal way to spend a weekend?",
    "Q4":"In a team, you're usually...",
    "Q5":"How do you approach risk?",
    "Q6":"Which best describes your thought process?",
    "Q7":"How do you react to conflict?",
    "Q8":"Which sounds more like you?",
    "Q9":"What’s your approach to goals?",
    **{f"Q{i}":"Red or Black?" for i in range(10, 16)}
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
    **{f"Q{i}": {"R": "Red", "B": "Black"} for i in range(10, 16)}
}

# == FUNCTIONS ==
def match_percent(p, ua):
    matches = sum(p[q] == ua[q] for q in p)
    return round(100 * matches / len(p), 1)

def generate_certificate(name, personality, percent):
    emoji = profile_descriptions[personality].split()[0]  # first emoji
    cert = Image.new("RGB", (700, 400), color="#f0f0f0")
    draw = ImageDraw.Draw(cert)
    title_font = ImageFont.load_default()
    
    draw.rectangle([0, 0, 700, 70], fill="#3366cc")
    draw.text((20, 20), f"🎓 Deep Personality Certificate", fill="white", font=title_font)
    draw.text((30, 100), f"Name: {name}", fill="black", font=title_font)
    draw.text((30, 150), f"Personality: {personality} {emoji}", fill="black", font=title_font)
    draw.text((30, 200), f"Match: {percent}%", fill="black", font=title_font)
    return cert

# == STREAMLIT APP ==
st.set_page_config(page_title="Deep Personality Quiz")
st.title("🌟 Deep Personality Quiz")

username = st.text_input("Enter your name to begin:")

if username:
    if st.button("Start Quiz"):
        user_answers = {}
        for qid, qtext in questions.items():
            answer = st.radio(f"{qtext}", list(options[qid].keys()), format_func=lambda x: options[qid][x], key=qid)
            user_answers[qid] = answer

        best, score = max(
            ((name, match_percent(p, user_answers)) for name, p in reference_profiles.items()),
            key=lambda x: x[1]
        )

        st.success(f"🎯 You are a {best}! ({score}% match)")
        st.markdown(profile_descriptions[best])

        cert = generate_certificate(username, best, score)
        st.image(cert, caption="📜 Your Personality Certificate")

        from io import BytesIO
        buf = BytesIO()
        cert.save(buf, format="PNG")
        st.download_button("📥 Download Certificate", data=buf.getvalue(), file_name="personality_certificate.png", mime="image/png")
