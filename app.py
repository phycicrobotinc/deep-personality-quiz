import streamlit as st
from datetime import datetime

# --- Questions including new life-related ones + final red/black questions ---
questions = [
    # Basic life info questions
    {"question": "What is your gender?", "options": ["Male", "Female", "Non-binary", "Prefer not to say"]},
    {"question": "What is your age group?", "options": ["Under 18", "18-24", "25-34", "35-44", "45-54", "55+"]},
    {"question": "What is your current financial status?", "options": ["Struggling", "Stable", "Comfortable", "Wealthy"]},
    {"question": "Do you enjoy social activities?", "options": ["Yes", "No"]},
    {"question": "Are you more of a morning or night person?", "options": ["Morning", "Night"]},
    {"question": "Do you prefer working alone or in a team?", "options": ["Alone", "Team"]},
    {"question": "How do you usually make decisions?", "options": ["Logic", "Emotion"]},
    {"question": "Do you consider yourself more introverted or extroverted?", "options": ["Introverted", "Extroverted"]},
    {"question": "Are you comfortable with taking risks?", "options": ["Yes", "No"]},
    {"question": "How often do you try new experiences?", "options": ["Often", "Sometimes", "Rarely"]},

    # Final 6 questions - Red or Black
    {"question": "Do you prefer Red or Black in card games?", "options": ["Red", "Black"]},
    {"question": "If you had to choose, would you wear Red or Black clothes?", "options": ["Red", "Black"]},
    {"question": "Do you feel more energetic wearing Red or Black?", "options": ["Red", "Black"]},
    {"question": "Which color do you associate with power, Red or Black?", "options": ["Red", "Black"]},
    {"question": "Which color do you think represents mystery better, Red or Black?", "options": ["Red", "Black"]},
    {"question": "In your opinion, which color is more elegant, Red or Black?", "options": ["Red", "Black"]},
]

# Personality types by score (dummy example)
personality_types = {
    "Red": "You are passionate, energetic, and bold.",
    "Black": "You are mysterious, elegant, and strong-willed.",
    "Mixed": "You have a balanced personality with both boldness and mystery."
}

def calculate_personality(answers):
    # Count red or black in last 6 answers
    red_black_answers = answers[-6:]
    red_count = red_black_answers.count("Red")
    black_count = red_black_answers.count("Black")
    if red_count > black_count:
        return "Red"
    elif bla
