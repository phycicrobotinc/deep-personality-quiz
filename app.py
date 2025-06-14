import streamlit as st

# Initialize session state variables if not present
if "submitted" not in st.session_state:
    st.session_state.submitted = False
if "answers" not in st.session_state:
    st.session_state.answers = {}
if "username" not in st.session_state:
    st.session_state.username = ""

# Questions dictionary (you can add more questions as needed)
questions = {
    "Q1": "What is your gender?",
    "Q2": "What is your age group?",
    "Q3": "What is your current employment status?",
    "Q4": "What is your approximate annual income?",
    "Q5": "How do you prefer to spend your free time?",
    "Q6": "Do you consider yourself more introverted or extroverted?",
    "Q7": "How important is financial security to you?",
    "Q8": "Do you enjoy trying new experiences?",
    "Q9": "Are you more analytical or creative?",
    "Q10": "Do you prefer red or black? (Final 6 questions start here)",
    "Q11": "Red or black?",
    "Q12": "Red or black?",
    "Q13": "Red or black?",
    "Q14": "Red or black?",
    "Q15": "Red or black?",
    "Q16": "Do you prefer working alone or in a team?",
    "Q17": "Are you more spontaneous or planned?",
    "Q18": "How often do you set long-term goals?",
}

# Options dictionary for each question
options = {
    "Q1": {"A": "Male", "B": "Female", "C": "Other", "D": "Prefer not to say"},
    "Q2": {"A": "Under 18", "B": "18-24", "C": "25-34", "D": "35-44", "E": "45+"},
    "Q3": {"A": "Employed full-time", "B": "Employed part-time", "C": "Student", "D": "Unemployed", "E": "Retired"},
    "Q4": {"A": "<$20,000", "B": "$20,000-$50,000", "C": "$50,001-$100,000", "D": ">$100,000"},
    "Q5": {"A": "Reading or relaxing", "B": "Sports or outdoor activities", "C": "Socializing", "D": "Creative hobbies"},
    "Q6": {"A": "Introverted", "B": "Extroverted"},
    "Q7": {"A": "Very important", "B": "Somewhat important", "C": "Not important"},
    "Q8": {"A": "Yes, I love new experiences", "B": "Sometimes", "C": "Rarely"},
    "Q9": {"A": "Analytical", "B": "Creative", "C": "Balanced"},
    "Q10": {"R": "Red", "B": "Black"},
    "Q11": {"R": "Red", "B": "Black"},
    "Q12": {"R": "Red", "B": "Black"},
    "Q13": {"R": "Red", "B": "Black"},
    "Q14": {"R": "Red", "B": "Black"},
    "Q15": {"R": "Red", "B": "Black"},
    "Q16": {"A": "Alone", "B": "Team"},
    "Q17": {"A": "Spontaneous", "B": "Planned"},
    "Q18": {"A": "Often", "B": "Sometimes", "C": "Rarely"},
}

# Personality types - simple example based on answers (you can customize logic)
def analyze_personality(answers):
    # Dummy example logic: count reds and blacks in final 6
    red_count = sum(1 for q in ["Q10","Q11","Q12","Q13","Q14","Q15"] if answers.get(q) == "R")
    black_count = 6 - red_count
    
    # Analyze gender as well for demo
    gender = answers.get("Q1", "Unknown")

    if red_count > black_count:
        personality = "You are adventurous and bold."
    elif black_count > red_count:
        personality = "You are calm and thoughtful."
    else:
        personality = "You have a balanced personality."
    
    return f"Hello {st.session_state.username}! {personality} Your gender is recorded as: {gender}."

# Main app
st.title("Deep Personality Quiz")

if not st.session_state.submitted:
    # Input username
    username = st.text_input("Please enter your name:", value=st.session_state.username, key="username")
    
    # Update username in session state if changed
    if username and username != st.session_state.username:
        st.session_state.username = username

    if usernam
