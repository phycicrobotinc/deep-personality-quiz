
import streamlit as st
import json
import os

# File to store/load profiles
PROFILES_FILE = "deep_profiles.json"

# Load or create reference profiles
if os.path.exists(PROFILES_FILE):
    with open(PROFILES_FILE, "r") as f:
        reference_profiles = json.load(f)
else:
    reference_profiles = {
        "Thinker": {
            "Q1": "B", "Q2": "A", "Q3": "B", "Q4": "A", "Q5": "C",
            "Q6": "B", "Q7": "D", "Q8": "A", "Q9": "C",
            "Q10": "R", "Q11": "B", "Q12": "R", "Q13": "B", "Q14": "R", "Q15": "R"
        },
        "Adventurer": {
            "Q1": "C", "Q2": "B", "Q3": "C", "Q4": "D", "Q5": "A",
            "Q6": "D", "Q7": "A", "Q8": "C", "Q9": "B",
            "Q10": "B", "Q11": "R", "Q12": "B", "Q13": "R", "Q14": "B", "Q15": "B"
        }
    }
    with open(PROFILES_FILE, "w") as f:
        json.dump(reference_profiles, f, indent=2)

# Profile descriptions
profile_descriptions = {
    "Thinker": (
        "You are methodical and rational.\n"
        "You analyze every decision, weigh pros and cons,\n"
        "and value logic over emotion."
    ),
    "Adventurer": (
        "You crave excitement and novelty.\n"
        "Spontaneity and challenge fuel your spirit,\n"
        "and you thrive on exploring the unknown."
    )
}

# Questions and answer options
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
    "Q10": "Red or Black?",
    "Q11": "Red or Black?",
    "Q12": "Red or Black?",
    "Q13": "Red or Black?",
    "Q14": "Red or Black?",
    "Q15": "Red or Black?"
}

options = {
    "Q1": {"A": "🧠 Emotional", "B": "📊 Logical", "C": "⚡ Impulsive", "D": "👥 Social"},
    "Q2": {"A": "🤫 Withdraw and reflect", "B": "📝 Plan better", "C": "🔄 Try again differently", "D": "🗣️ Talk it out"},
    "Q3": {"A": "📚 Reading alone", "B": "🧪 Learning a skill", "C": "✈️ Spontaneous trip", "D": "🎉 Party or gathering
