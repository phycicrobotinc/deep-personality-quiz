import streamlit as st
import random
import json
import os

# == SETUP ==
st.set_page_config(page_title="Deep Personality Quiz", page_icon="🌟")
st.title("🌟 Deep Personality Quiz")
st.write("Answer each question to discover which profile best matches you!")

# == QUESTION DATA ==
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
    q: dict(opts) for q, opts in {
        "Q1": [("A", "🧠 Emotional"), ("B", "📊 Logical"), ("C", "⚡ Impulsive"), ("D", "👥 Social")],
        "Q2": [("A", "🤫 Withdraw and reflect"), ("B", "📝 Plan better"), ("C", "🔄 Try again differently"), ("D", "🗣️ Talk it out")],
        "Q3": [("A", "📚 Reading alone"), ("B", "🧪 Learning a skill"), ("C", "✈️ Spontaneous trip"), ("D", "🎉 Party or gathering")],
        "Q4": [("A", "📋 Organizer"), ("B", "🧠 Strategist"), ("C", "🌀 Wild card"), ("D", "🧭 Leader")],
        "Q5": [("A", "📈 Calculated risks"), ("B", "🛑 Avoid risks"), ("C", "🎢 Chase thrill"), ("D", "🌀 Depends on mood")],
        "Q6": [("A", "📐 Structured"), ("B", "📊 Analytical"), ("C", "🌊 Flexible"), ("D", "🌌 Abstract")],
        "Q7": [("A", "🚪 Avoid"), ("B", "🤝 Negotiate"), ("C", "⚔️ Challenge"), ("D", "🧘 Calm and listen")],
        "Q8": [("A", "🗂️ Planned"), ("B", "💓 Emotional"), ("C", "🌈 Free-spirited"), ("D", "🏁 Driven")],
        "Q9": [("A", "📋 Lists"), ("B", "💭 Dream big"), ("C", "🔁 Adapt"), ("D", "🎯 Visualize and go")],
        **{f"Q{i}": [("R", "🔴 Red"), ("B", "⚫ Black")] for i in range(10, 16)}
    }.items()
}

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

profile_descriptions = {
    "Thinker": """🧠 You are methodical and rational.
You analyze every decision, weigh pros and cons, and value logic over emotion.""",
    "Adventurer": """✈️ You crave excitement and novelty.
Spontaneity and challenge fuel your spirit, and you thrive on exploring the unknown."""
}

# == FUNCTIONS ==
def match_percent(pref, ua):
    matches = sum(pref[q] == ua[q] for q in pref)
    return round(100 * matches / len(pref), 1)

def get_best_match(user_answers):
    best, best_score = max(
        ((name, match_percent(p, user_answers)) for name, p in reference_profiles.items()),
        key=lambda x: x[1]
    )
    return best, best_score

def generate_profile_description(name):
    return profile_descriptions.get(name, f"🧩 You are unique! This profile doesn't have a predefined description yet, but your answers show you're original and complex.")

# == UI ==
user_answers = {}
with st.form("quiz_form"):
    for idx, (qid, qtext) in enumerate(questions.items(), 1):
        st.markdown(f"**{idx}. {qtext}**")
        choices = options[qid]
        user_answers[qid] = st.radio("", list(choices.keys()), format_func=lambda k: choices[k], key=qid)
    submitted = st.form_submit_button("Submit")

if submitted:
    best, score = get_best_match(user_answers)
    st.subheader("🎯 Your Best Match:")
    st.success(f"**{best}** – {score}% match")
    st.markdown(generate_profile_description(best))

    # Display all match percentages
    st.markdown("---")
    st.markdown("### 🔍 Match Scores")
    for name, profile in reference_profiles.items():
        pct = match_percent(profile, u_
