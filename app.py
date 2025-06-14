import streamlit as st

# Initialize session state variables if not present
if "submitted" not in st.session_state:
    st.session_state.submitted = False
if "answers" not in st.session_state:
    st.session_state.answers = {}
if "username" not in st.session_state:
    st.session_state.username = ""

# Questions dictionary with red/black questions spaced out
questions = {
    "Q1": "What is your gender?",
    "Q2": "What is your age group?",
    "Q3": "What is your current employment status?",
    "Q4": "Red or Black?",
    "Q5": "What is your approximate annual income?",
    "Q6": "How do you prefer to spend your free time?",
    "Q7": "Red or Black?",
    "Q8": "Do you consider yourself more introverted or extroverted?",
    "Q9": "How important is financial security to you?",
    "Q10": "Red or Black?",
    "Q11": "Do you enjoy trying new experiences?",
    "Q12": "Are you more analytical or creative?",
    "Q13": "Red or Black?",
    "Q14": "Do you prefer working alone or in a team?",
    "Q15": "Are you more spontaneous or planned?",
    "Q16": "Red or Black?",
}

# Options for each question (placeholder option will be added dynamically)
options = {
    "Q1": ["Male", "Female", "Other", "Prefer not to say"],
    "Q2": ["Under 18", "18-24", "25-34", "35-44", "45+"],
    "Q3": ["Employed full-time", "Employed part-time", "Student", "Unemployed", "Retired"],
    "Q4": ["Red", "Black"],
    "Q5": ["<$20,000", "$20,000-$50,000", "$50,001-$100,000", ">$100,000"],
    "Q6": ["Reading or relaxing", "Sports or outdoor activities", "Socializing", "Creative hobbies"],
    "Q7": ["Red", "Black"],
    "Q8": ["Introverted", "Extroverted"],
    "Q9": ["Very important", "Somewhat important", "Not important"],
    "Q10": ["Red", "Black"],
    "Q11": ["Yes, I love new experiences", "Sometimes", "Rarely"],
    "Q12": ["Analytical", "Creative", "Balanced"],
    "Q13": ["Red", "Black"],
    "Q14": ["Alone", "Team"],
    "Q15": ["Spontaneous", "Planned"],
    "Q16": ["Red", "Black"],
}

def analyze_personality(answers):
    # Count red/black answers from the red/black questions
    red_qs = ["Q4", "Q7", "Q10", "Q13", "Q16"]
    red_count = sum(1 for q in red_qs if answers.get(q) == "Red")
    black_count = len(red_qs) - red_count
    
    # Use gender as example info
    gender = answers.get("Q1", "Unknown")
    
    if red_count > black_count:
        personality = "You are adventurous and bold."
    elif black_count > red_count:
        personality = "You are calm and thoughtful."
    else:
        personality = "You have a balanced personality."
    
    return f"Hello {st.session_state.username}! {personality} Your gender is recorded as: {gender}."

def show_certificate():
    st.markdown("---")
    st.header("Your Personality Certificate")
    st.markdown(f"""
    **Name:** {st.session_state.username}  
    **Result:** {analyze_personality(st.session_state.answers)}  
    """)
    st.balloons()

# --- Streamlit app UI ---

st.title("Deep Personality Quiz")

if not st.session_state.submitted:
    # Username input (required)
    username = st.text_input("Please enter your name:", value=st.session_state.username)
    if username != st.session_state.username:
        st.session_state.username = username
    
    if not username:
        st.warning("Please enter your name to continue.")
        st.stop()

    # Questions with placeholder forcing user selection
    for qid, qtext in questions.items():
        opts = options[qid]
        placeholder = "-- Select an option --"
        select_options = [placeholder] + opts
        
        current_answer = st.session_state.answers.get(qid, placeholder)
        
        answer = st.selectbox(
            qtext,
            select_options,
            index=select_options.index(current_answer) if current_answer in select_options else 0,
            key=qid
        )
        
        if answer != placeholder:
            st.session_state.answers[qid] = answer
        else:
            # Remove answer if placeholder selected
            st.session_state.answers.pop(qid, None)
    
    # Submit button and validation
    if st.button("Submit"):
        unanswered = [q for q in questions if q not in st.session_state.answers]
        if unanswered:
            st.error(f"Please answer all questions before submitting. Missing: {', '.join(unanswered)}")
        else:
            st.session_state.submitted = True
            st.success("Thank you for completing the quiz!")
            show_certificate()

else:
    # After submission, show certificate and allow reset
    show_certificate()
    
    if st.button("Retake Quiz"):
        st.session_state.submitted = False
        st.session_state.answers = {}
        st.experimental_rerun()
