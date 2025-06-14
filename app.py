import os
import json
import random
import streamlit as st

# Setup data folder and file for profiles (adjust path if needed)
DATA_FOLDER = "PersonalityQuizData"
os.makedirs(DATA_FOLDER, exist_ok=True)
PROFILES_FILE = os.path.join(DATA_FOLDER, "deep_profiles.json")

# Load or create reference profiles
if os.path.exists(PROFILES_FILE):
    with open(PROFILES_FILE, "r") as f:
        reference_profiles = json.load(f)
else:
    reference_profiles = {
        "Thinker": {
            "Q1": "B","Q2": "A","Q3": "B","Q4": "A","Q5": "C",
            "Q6": "B","Q7": "D","Q8": "A","Q9": "C",
            "Q10":"R","Q11":"B","Q12":"R","Q13":"B","Q14":"R","Q15":"R"
        },
        "Adventurer": {
            "Q1": "C","Q2": "B","Q3": "C","Q4": "D","Q5": "A",
            "Q6": "D","Q7": "A","Q8": "C","Q9": "B",
            "Q10":"B","Q11":"R","Q12":"B","Q13":"R","Q14":"B","Q15":"B"
        }
    }
    with open(PROFILES_FILE, "w") as f:
        json.dump(reference_profiles, f, indent=2)

# Questions & Options
questions = {
    "Q1":"How do you make decisions?",
    "Q2":"How do you handle failure?",
    "Q3":"Your ideal way to spend a weekend?",
    "Q4":"In a team, you're usually...",
    "Q5":"How do you approach risk?",
    "Q6":"Which best describes your thought process?",
    "Q7":"How do you react to conflict?",
    "Q8":"Which sounds more like you?",
    "Q9":"What’s your approach to goals?",
    "Q10":"Red or Black?",
    "Q11":"Red or Black?",
    "Q12":"Red or Black?",
    "Q13":"Red or Black?",
    "Q14":"Red or Black?",
    "Q15":"Red or Black?"
}

options = {
    "Q1": {"A": "🧠 Emotional", "B": "📊 Logical", "C": "⚡ Impulsive", "D": "👥 Social"},
    "Q2": {"A": "🤫 Withdraw and reflect", "B": "📝 Plan better", "C": "🔄 Try again differently", "D": "🗣️ Talk it out"},
    "Q3": {"A": "📚 Reading alone", "B": "🧪 Learning a skill", "C": "✈️ Spontaneous trip", "D": "🎉 Party or gathering"},
    "Q4": {"A": "📋 Organizer", "B": "🧠 Strategist", "C": "🌀 Wild card", "D": "🧭 Leader"},
    "Q5": {"A": "📈 Calculated risks", "B": "🛑 Avoid risks", "C": "🎢 Chase thrill", "D": "🌀 Depends on mood"},
    "Q6": {"A": "📐 Structured", "B": "📊 Analytical", "C": "🌊 Flexible", "D": "🌌 Abstract"},
    "Q7": {"A": "🚪 Avoid", "B": "🤝 Negotiate", "C": "⚔️ Challenge", "D": "🧘 Calm and listen"},
    "Q8": {"A": "🗂️ Planned", "B": "💓 Emotional", "C": "🌈 Free-spirited", "D": "🏁 Driven"},
    "Q9": {"A": "📋 Lists", "B": "💭 Dream big", "C": "🔁 Adapt", "D": "🎯 Visualize and go"},
    "Q10": {"R": "🔴 Red", "B": "⚫ Black"},
    "Q11": {"R": "🔴 Red", "B": "⚫ Black"},
    "Q12": {"R": "🔴 Red", "B": "⚫ Black"},
    "Q13": {"R": "🔴 Red", "B": "⚫ Black"},
    "Q14": {"R": "🔴 Red", "B": "⚫ Black"},
    "Q15": {"R": "🔴 Red", "B": "⚫ Black"},
}

# Profile descriptions for all profiles including generic for new users
profile_descriptions = {
    "Thinker": """You are methodical and rational.
You analyze every decision, weigh pros and cons,
and value logic over emotion.""",
    "Adventurer": """You crave excitement and novelty.
Spontaneity and challenge fuel your spirit,
and you thrive on exploring the unknown.""",
}

# For user profiles that are new and saved later
def get_profile_description(name):
    return profile_descriptions.get(name, 
        "You have a unique combination of traits.\n"
        "Explore yourself and maybe share your results to enrich our profiles!")

# Calculate match %
def match_percent(profile, user_answers):
    matches = sum(profile.get(q) == user_answers.get(q) for q in profile)
    return round(100 * matches / len(profile), 1)

# Save new user profile if unique
def save_profile(user_answers):
    # Avoid duplicate
    if user_answers in reference_profiles.values():
        return None
    i = 1
    while f"UserProfile_{i}" in reference_profiles:
        i += 1
    name = f"UserProfile_{i}"
    reference_profiles[name] = user_answers
    with open(PROFILES_FILE, "w") as f:
        json.dump(reference_profiles, f, indent=2)
    return name

# Streamlit UI
def main():
    st.title("🌟 Deep Personality Quiz 🌟")
    st.write("Answer the questions below:")

    user_answers = {}

    for qid, qtext in questions.items():
        opts = options[qid]
        choice = st.radio(f"{qtext}", list(opts.values()), key=qid)
        # Reverse lookup: get key from value
        selected_key = next(k for k, v in opts.items() if v == choice)
        user_answers[qid] = selected_key

    if st.button("Submit"):
        # Find best match profile
        best_name = None
        best_score = -1
        for prof_name, prof_answers in reference_profiles.items():
            score = match_percent(prof_answers, user_answers)
            if score > best_score:
                best_score = score
                best_name = prof_name
        
        st.markdown("---")
        st.subheader(f"🎯 Best Match: {best_name} ({best_score}%)")
        st.write(get_profile_description(best_name))

        # Save user profile if new
        saved_name = save_profile(user_answers)
        if saved_name:
            st.success(f"💾 Your unique profile was saved as {saved_name}")
        else:
            st.info("Your profile matches an existing one, so it was not saved again.")

if __name__ == "__main__":
    main()
