import streamlit as st
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO

# == PERSONALITY PROFILES ==
reference_profiles = {
    "Thinker":     {"Q1": "B", "Q2": "B", "Q3": "A", "Q4": "B", "Q5": "B", "Q6": "B", "Q7": "B", "Q8": "A", "Q9": "A", 
                    "Q10": "R", "Q11": "B", "Q12": "R", "Q13": "B", "Q14": "R", "Q15": "B"},
    "Adventurer":  {"Q1": "C", "Q2": "C", "Q3": "C", "Q4": "C", "Q5": "C", "Q6": "C", "Q7": "C", "Q8": "C", "Q9": "C", 
                    "Q10": "B", "Q11": "R", "Q12": "B", "Q13": "R", "Q14": "B", "Q15": "R"},
    "Empath":      {"Q1": "A", "Q2": "D", "Q3": "D", "Q4": "A", "Q5": "D", "Q6": "D", "Q7": "A", "Q8": "B", "Q9": "B", 
                    "Q10": "R", "Q11": "R", "Q12": "R", "Q13": "R", "Q14": "B", "Q15": "B"},
    "Innovator":   {"Q1": "D", "Q2": "C", "Q3": "B", "Q4": "D", "Q5": "A", "Q6": "A", "Q7": "D", "Q8": "D", "Q9": "D", 
                    "Q10": "B", "Q11": "B", "Q12": "B", "Q13": "R", "Q14": "R", "Q15": "B"},
    "Leader":      {"Q1": "B", "Q2": "A", "Q3": "D", "Q4": "D", "Q5": "A", "Q6": "A", "Q7": "D", "Q8": "D", "Q9": "D", 
                    "Q10": "B", "Q11": "B", "Q12": "R", "Q13": "B", "Q14": "R", "Q15": "B"},
    "Visionary":   {"Q1": "D", "Q2": "C", "Q3": "B", "Q4": "B", "Q5": "C", "Q6": "D", "Q7": "C", "Q8": "B", "Q9": "B", 
                    "Q10": "R", "Q11": "R", "Q12": "B", "Q13": "B", "Q14": "R", "Q15": "R"},
    "Analyst":     {"Q1": "B", "Q2": "B", "Q3": "A", "Q4": "B", "Q5": "A", "Q6": "B", "Q7": "B", "Q8": "A", "Q9": "A", 
                    "Q10": "B", "Q11": "B", "Q12": "R", "Q13": "B", "Q14": "B", "Q15": "B"},
    "Seeker":      {"Q1": "C", "Q2": "C", "Q3": "C", "Q4": "C", "Q5": "C", "Q6": "C", "Q7": "A", "Q8": "C", "Q9": "C", 
                    "Q10": "R", "Q11": "R", "Q12": "R", "Q13": "R", "Q14": "R", "Q15": "R"},
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
    **{f"Q{i}": "Red or Black?" for i in range(10, 16)}
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
    **{f"Q{i}": {"R": "Red", "B": "Black"} for i in range(10, 16)}
}

# == FUNCTIONS ==
def match_percent(profile, user_answers):
    matches = sum(profile[q] == user_answers.get(q, "") for q in profile)
    return round(100 * matches / len(profile), 1)

def generate_certificate(name, personality, percent):
    emoji = profile_descriptions[personality].split()[0]  # first emoji
    cert = Image.new("RGB", (700, 400), color="#f0f0f0")
    draw
