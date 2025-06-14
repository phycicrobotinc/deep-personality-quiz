import streamlit as st

# Initialize session state variables if not present
if "submitted" not in st.session_state:
    st.session_state.submitted = False
if "answers" not in st.session_state:
    st.session_state.answers = {}
if "username" not in st.session_state:
    st.session_state.username = ""

# Questions with red/black questions spaced every 3 questions
questions = {
    "Q1": "What is your gender?",
    "Q2": "What is your age group?",
    "Q3": "What is your current employment status?",
    "Q4": "Do you prefer red or black? (Red/Black question #1)",
    "Q5": "What is your approximate annual income?",
    "Q6": "How do you prefer to spend your free time?",
    "Q7": "Do you prefer red or black? (Red/Black question #2)",
    "Q8": "Do you consider yourself more introverted or extroverted?",
    "Q9": "How important is financial security to you?",
    "Q10": "Do you prefer red or black? (Red/Black question #3)",
    "Q11": "Do you enjoy trying new experiences?",
    "Q12": "Are you more analytical or creative?",
    "Q13": "Do you prefer red or black? (Red/Black question #4)",
    "Q14": "Do you prefer working alone or in a team?",
    "Q15": "Are you more spontaneous or planned?",
    "Q16": "Do you prefer red or black? (Red/Black question #5)",
    "Q17": "How often do you set long-term goals?",
    "Q18": "Do you prefer red or black? (Red/Black question #6)",
}

# Options for each question
options = {
    "Q1": {"A": "Male", "B": "Female", "C": "Other", "D": "Prefer not to say"},
    "Q2": {"A": "Under 18", "B": "18-24", "C": "25-34", "D": "35-44", "E": "45+"},
    "Q3": {"A": "Employed full-time", "B": "Employed part-time", "C": "Student", "D": "Unemployed", "E": "Retired"},
    "Q4": {"R": "Red", "B": "Black"},
    "Q5": {"A": "<$20,000", "B": "$20,000-$50,000", "C": "$50,001-$100,000", "D": ">$100,000"},
    "Q6": {"A": "Reading or relaxing", "B": "Sports or outdoor activities", "C": "Socializing", "D": "Creative hobbies"},
    "Q7": {"R": "Red", "B": "Black"},
    "Q8": {"A": "Introverted", "B": "Extroverted"},
    "Q9": {"A": "Very important", "B": "Somewhat important", "C": "Not important"},
    "Q10": {"R": "Red", "B": "Black"},
    "Q11": {"A": "Yes, I love new experiences", "B": "Sometimes", "C": "Rarely"},
    "Q12": {"A": "Analytical", "B": "Creative", "C": "Balanced"},
    "Q13": {"R": "Red", "B": "Black"},
    "Q14": {"A": "Alone", "B": "Team"},
    "Q15": {"A": "Spontaneous", "B": "Planned"},
    "Q16": {"R": "Red", "B": "Black"},
    "Q17": {"A": "Often", "B": "Sometimes", "C": "Rarely"},
    "Q18": {"R": "Red", "B": "Black"},
}

# Personality analysis logic
def analyze_personality(answers):
    red_count = sum(1 for q in ["Q4","Q7","Q10","Q13","Q16","Q18"] if answers.get(q) == "R")
    black_count = 6 - red_count
    gender = answers.get("Q1", "Unknown")

    if red_count > black_count:
        personality = "You are adventurous and bold."
    elif black_count > red_count:
        personality = "You are calm and thoughtful."
    else:
        personality = "You have a balanced personality."

    return f"Hello {st.session_state.username}! {personality} Your gender is recorded as: {gender}."

# App title
st.title("Deep Personality Quiz")

if not st.session_state.submitted:
    # Input username
    username = st.text_input("Please enter your name:", value=st.session_state.username, key="username")

    # Update username in session state if changed
    if username and username != st.session_state.username:
        st.session_state.username = username

    if username:
        st.markdown("### Please answer all questions:")
        # Show questions with placeholder
        all_answered = True
        placeholder = "-- Select an option --"
        for qid, qtext in questions.items():
            opts = options[qid]
            select_options = [placeholder] + [opts[k] for k in opts]
            # Get stored answer or placeholder
            stored_answer = st.session_state.answers.get(qid, placeholder)
            # Determine index to show selected answer or placeholder
            index = 0
            if stored_answer in select_options:
                index = select_options.index(stored_answer)
            answer = st.selectbox(qtext, select_options, index=index, key=qid)
            if answer == placeholder:
                all_answered = False
                # Remove any old answer
                if qid in st.session_state.answers:
                    del st.session_state.answers[qid]
            else:
                st.session_state.answers[qid] = answer

        # Only allow submission if all answered
        if all_answered:
            if st.button("Submit"):
                st.session_state.submitted = True
        else:
            st.warning("Please answer all questions before submitting.")

else:
    # Show personality result
    result = analyze_personality(st.session_state.answers)
    st.success(result)

    # Show certificate (simple version)
    st.markdown("---")
    st.markdown(f"""
    ### Certificate of Completion

    This certifies that **{st.session_state.username}** has completed the Deep Personality Quiz.

    **Result:** {result}
    """)
    if st.button("Retake Quiz"):
        st.session_state.submitted = False
        st.session_state.answers = {}
        st.experimental_rerun()
