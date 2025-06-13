import streamlit as st
import json
import random
import os

# Load reference profiles from JSON or create them
PROFILES_FILE = "deep_profiles.json"

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
    with open(PROFILES_FILE, "w") as_
