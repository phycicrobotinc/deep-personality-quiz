import streamlit as st

# Initialize session state variables once
if "submitted" not in st.session_state:
    st.session_state.submitted = False
if "answers" not in st.session_state:
    st.session_state.answers = {}
if "username" not in st.session_state:
    st.session_state.username = ""

# Questions with Red/Black spaced every 3 questions
questions_order = [
    "Q1", "Q2", "Q3", "Q4",  # Red/Black Q4
    "Q5", "Q6", "Q7",        # Red/Black Q7
    "Q8", "Q9", "Q10",       # Red/Black Q10
    "Q11", "Q12", "Q13",     # Red/Black Q13
    "Q14", "Q15", "Q16",     # Red/Black Q16
    "Q17", "Q18"             # Red/Black Q18
]

questions = {
    "Q1": "What is your gender?",
    "Q2": "What is your age group?",
    "Q3": "What is your current employment status?",
    "Q4": "Do you prefer red or black? (Question 1)",
    "Q5": "What is your approximate annual income?",
    "Q6": "How do you prefer to spend your free time?",
    "Q7": "Do you prefer red or black? (Question 2)",
    "Q8": "Do you consider yourself more introverted or extroverted?",
    "Q9": "How important is financial security to you?",
    "Q10": "Do you prefer red or black? (Question 3)",
    "Q11": "Do you enjoy trying new experiences?",
    "Q12": "Are you more analytical or creative?",
    "Q13": "Do you prefer red or black? (Question 4)",
    "Q14": "Do you prefer working alone or in a team?",
    "Q15": "Are you more spontaneous or planned?",
    "Q16": "Do you prefer red or black? (Question 5)",
    "Q17": "How often do you set long-term goals?",
    "Q18": "Do you prefer red or black? (Question 6)",
}

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
    "Q17": ["Often", "Sometimes", "Rarely"],
    "Q18": ["Red", "Black"],
}

def analyze_personality(answers):
    # Count how many reds and blacks
    red_questions = ["Q4", "Q7", "Q10", "Q13", "Q16", "Q18"]
    red_count = sum(1 for q in red_questions if answers.get(q) == "Red")
    black_count = len(red_questions) - red_count

    gender = answers.get("Q1", "Unknown")
    age = answers.get("Q2", "Unknown")
    employment = answers.get("Q3", "Unknown")

    personality_desc = ""
    if red_count > black_count:
        personality_desc = "You are adventurous, bold, and take risks."
    elif black_count > red_count:
        personality_desc = "You are calm, thoughtful, and prefer stability."
    else:
        personality_desc = "You have a balanced personality with a mix of boldness and calm."

    extra = f"\n\nGender: {gender}\nAge group: {age}\nEmployment status: {employment}"

    return personality_desc + extra

st.title("Deep Personality Quiz")

if not st.session_state.submitted:
    # Input username
    username = st.text_input("Please enter your name:", value=st.session_state.username, key="username")

    if username:
        st.session_state.username = username

        st.markdown("### Please answer all the questions below:")

        all_answered = True
        for qid in questions_order:
            qtext = questions[qid]
            opts = options[qid]

            # Get previously selected answer or None
            prev_answer = st.session_state.answers.get(qid, None)

            # Use selectbox with no default selection (index -1 not allowed, so trick: add dummy option)
            choice = st.selectbox(qtext, ["-- Select an option --"] + opts, index=0, key=qid)

            if choice == "-- Select an option --":
                all_answered = False
                # Remove old answer if any
                if qid in st.session_state.answers:
                    del st.session_state.answers[qid]
            else:
                st.session_state.answers[qid] = choice

        if not all_answered:
            st.warning("Please answer all questions to enable submission.")
        else:
            if st.button("Submit"):
                st.session_state.submitted = True
                st.experimental_rerun()

else:
    # Show results
    st.success(f"Thank you for completing the quiz, {st.session_state.username}!")
    result_text = analyze_personality(st.session_state.answers)
    st.write(result_text)

    # Simple certificate
    st.markdown("---")
    st.markdown(f"""
    ### Certificate of Completion

    This certifies that **{st.session_state.username}** has completed the Deep Personality Quiz.

    **Personality Summary:** {result_text}
    """)

    if st.button("Retake Quiz"):
        st.session_state.submitted = False
        st.session_state.answers = {}
        st.experimental_rerun()
