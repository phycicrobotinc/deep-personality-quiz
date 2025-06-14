import streamlit as st
import datetime

# --- Questions Section ---
questions = [
    # New life-related questions
    {"question": "What is your gender?", "options": ["Male", "Female", "Other"]},
    {"question": "What is your age group?", "options": ["Under 18", "18-24", "25-34", "35-44", "45-54", "55+"]},
    {"question": "What is your current employment status?", "options": ["Employed", "Unemployed", "Student", "Retired"]},
    {"question": "How would you describe your financial status?", "options": ["Low income", "Middle income", "High income"]},
    {"question": "What is your highest level of education?", "options": ["High school", "College", "University", "Postgraduate"]},
    {"question": "Do you live in an urban or rural area?", "options": ["Urban", "Rural"]},
    {"question": "Are you currently in a relationship?", "options": ["Yes", "No", "Prefer not to say"]},
    {"question": "How often do you exercise?", "options": ["Daily", "Weekly", "Monthly", "Rarely"]},
    {"question": "How do you prefer to spend your free time?", "options": ["Alone", "With friends", "With family", "Online"]},
    # Original personality questions (example, you can expand)
    {"question": "I enjoy social gatherings.", "options": ["Agree", "Neutral", "Disagree"]},
    {"question": "I prefer planning over spontaneity.", "options": ["Agree", "Neutral", "Disagree"]},
    {"question": "I often think about the future.", "options": ["Agree", "Neutral", "Disagree"]},
    {"question": "I like to take risks.", "options": ["Agree", "Neutral", "Disagree"]},
    # Last 6 Red or Black questions (unchanged)
    {"question": "Choose Red or Black: Question 1", "options": ["Red", "Black"]},
    {"question": "Choose Red or Black: Question 2", "options": ["Red", "Black"]},
    {"question": "Choose Red or Black: Question 3", "options": ["Red", "Black"]},
    {"question": "Choose Red or Black: Question 4", "options": ["Red", "Black"]},
    {"question": "Choose Red or Black: Question 5", "options": ["Red", "Black"]},
    {"question": "Choose Red or Black: Question 6", "options": ["Red", "Black"]},
]

# --- Personality Descriptions ---
descriptions = {
    "Type A": "You are energetic and ambitious.",
    "Type B": "You are relaxed and easy-going.",
    "Type C": "You are detail-oriented and thoughtful.",
    "Type D": "You are cautious and reserved.",
    "Red": "You choose red — passionate and bold.",
    "Black": "You choose black — mysterious and strong.",
}

# --- Helper function to calculate personality ---
def calculate_personality(answers):
    # Simple demo logic:
    red_black_answers = answers[-6:]
    reds = red_black_answers.count("Red")
    blacks = red_black_answers.count("Black")
    if reds > blacks:
        return "Red"
    elif blacks > reds:
        return "Black"
    else:
        # Just a fallback for demonstration
        return "Type A"

# --- Streamlit App ---
st.title("🧠 Deep Personality Quiz")

answers = []

for i, q in enumerate(questions):
    answer = st.radio(f"Q{i+1}. {q['question']}", q["options"], key=f"q{i}")
    answers.append(answer)

if st.button("Submit"):
    personality = calculate_personality(answers)
    st.write(f"## 🎉 Your Personality Type is: {personality}")
    if personality in descriptions:
        st.write(descriptions[personality])
    
    st.markdown("---")
    st.subheader("📜 Your Personalized Certificate")
    
    user_name = st.text_input("Enter your name for the certificate:")

    if user_name:
        today = datetime.date.today().strftime("%B %d, %Y")
        st.markdown(f"""
        <div style="border: 3px solid #4CAF50; padding: 30px; border-radius: 15px; text-align: center; background-color: #f9f9f9;">
            <h2 style="color: #2E8B
