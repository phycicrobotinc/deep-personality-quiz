import streamlit as st
import random
import datetime

# Define all the questions (the final 6 must remain red or black)
questions = [
    "What is your age?",
    "What is your gender identity?",
    "What is your current financial status?",
    "How satisfied are you with your current career or occupation?",
    "How often do you feel stressed in a typical week?",
    "What is your relationship status?",
    "How many close friends do you have?",
    "Do you consider yourself more introverted or extroverted?",
    "Do you prefer routine or spontaneity?",
    "Do you make decisions more based on logic or emotions?",
    "Do you enjoy working in teams or alone?",
    "Are you more future-focused or present-minded?",
    "Do you value tradition or innovation more?",
    "Are you more of a planner or a go-with-the-flow type?",
    "Would you rather read a book or attend a party?",
    "Do you trust people easily?",
    "Do you handle change we
# Streamlit app starts here
st.title("🌟 Deep Personality Quiz")
st.markdown("Answer the following questions to reveal your deep personality profile.")

responses = {}

with st.form("quiz_form"):
    for q in questions:
        if q in choices:
            responses[q] = st.selectbox(q, choices[q])
        else:
            responses[q] = st.text_input(q)

    submitted = st.form_submit_button("Submit")

if submitted:
    personality = determine_personality(responses)
    st.subheader(f"🧠 Your Personality Type: {personality}")
    st.write(personality_types[personality])

    st.markdown("---")
    st.subheader("📜 Your Certificate")

    user_name = st.text_input("Enter your name for the certificate:")
    if user_name:
        today = datetime.date.today().strftime("%B %d, %Y")
        st.markdown(f"""
        ### 🎉 Certificate of Completion  
        **This certifies that**  
        ### *{user_name}*  
        **has completed the Deep Personality Quiz on {today}**  
        and has been identified as  
        ## 🧠 {personality}  
        ---
        """)
