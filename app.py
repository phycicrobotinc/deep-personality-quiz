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
    "Do you handle change well?",
    "Are you more ambitious or content?",
    "Do you spend money freely or cautiously?",
    "Do you often reflect on the meaning of life?",

    # The 6 mandatory "Red or Black" questions
    "Red or Black? (1)",
    "Red or Black? (2)",
    "Red or Black? (3)",
    "Red or Black? (4)",
    "Red or Black? (5)",
    "Red or Black? (6)",
]

# Define possible answers for multiple choice
choices = {
    "What is your age?": ["Under 18", "18-24", "25-34", "35-44", "45-54", "55+"],
    "What is your gender identity?": ["Male", "Female", "Non-binary", "Prefer not to say"],
    "What is your current financial status?": ["Struggling", "Stable", "Comfortable", "Wealthy"],
    "How satisfied are you with your current career or occupation?": ["Very satisfied", "Somewhat", "Neutral", "Dissatisfied"],
    "How often do you feel stressed in a typical week?": ["Rarely", "Sometimes", "Often", "Always"],
    "What is your relationship status?": ["Single", "In a relationship", "Married", "Complicated"],
    "How many close friends do you have?": ["0", "1-2", "3-5", "6+"],
    "Do you consider yourself more introverted or extroverted?": ["Introverted", "Extroverted", "Depends"],
    "Do you prefer routine or spontaneity?": ["Routine", "Spontaneity", "Mix of both"],
    "Do you make decisions more based on logic or emotions?": ["Logic", "Emotions", "Both equally"],
    "Do you enjoy working in teams or alone?": ["Teams", "Alone", "Either"],
    "Are you more future-focused or present-minded?": ["Future-focused", "Present-minded", "Both"],
    "Do you value tradition or innovation more?": ["Tradition", "Innovation", "Depends"],
    "Are you more of a planner or a go-with-the-flow type?": ["Planner", "Go with the flow", "Both"],
    "Would you rather read a book or attend a party?": ["Read a book", "Attend a party", "Depends"],
    "Do you trust people easily?": ["Yes", "No", "Sometimes"],
    "Do you handle change well?": ["Yes", "No", "Sometimes"],
    "Are you more ambitious or content?": ["Ambitious", "Content", "Both"],
    "Do you spend money freely or cautiously?": ["Freely", "Cautiously", "Depends"],
    "Do you often reflect on the meaning of life?": ["Often", "Sometimes", "Rarely"],

    # Red or Black questions
    "Red or Black? (1)": ["Red", "Black"],
    "Red or Black? (2)": ["Red", "Black"],
    "Red or Black? (3)": ["Red", "Black"],
    "Red or Black? (4)": ["Red", "Black"],
    "Red or Black? (5)": ["Red", "Black"],
    "Red or Black? (6)": ["Red", "Black"],
}

# Define personality types and review summaries
personality_types = {
    "The Analyst": "You are thoughtful, strategic, and value logic and analysis. You enjoy exploring complex ideas and often seek knowledge.",
    "The Diplomat": "You are empathetic, creative, and focused on harmony
