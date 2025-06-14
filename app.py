import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import io

# ---------------------- INIT STATE ----------------------
if "submitted" not in st.session_state:
    st.session_state.submitted = False
if "answers" not in st.session_state:
    st.session_state.answers = {}
if "username" not in st.session_state:
    st.session_state.username = ""

# ---------------------- QUESTIONS ----------------------
questions = {
    1: "What is your gender?",
    2: "What is your age group?",
    3: "What is your current employment status?",
    4: "What is your approximate annual income?",
    5: "What is your favorite way to spend weekends?",
    6: "Red or Black?",
    7: "Do you consider yourself more introverted or extroverted?",
    8: "Do you enjoy trying new experiences?",
    9: "Red or Black?",
    10: "Are you more analytical or creative?",
    11: "Do you prefer working alone or in a team?",
    12: "Red or Black?",
    13: "Are you more spontaneous or planned?",
    14: "How often do you set long-term goals?",
    15: "Red or Black?",
    16: "Do you often reflect on your emotions?",
    17: "How important is financial security to you?",
    18: "Red or Black?",
    19: "Do you make decisions quickly or after lots of thought?",
    20: "What drives you most in life?"
}

options = {
    1: {"A": "Male", "B": "Female", "C": "Other", "D": "Prefer not to say"},
    2: {"A": "Under 18", "B": "18-24", "C": "25-34", "D": "35-44", "E": "45+"},
    3: {"A": "Employed full-time", "B": "Part-time", "C": "Student", "D": "Unemployed", "E": "Retired"},
    4: {"A": "<20k", "B": "20k-50k", "C": "50k-100k", "D": ">100k"},
    5: {"A": "Reading/relaxing", "B": "Sports", "C": "Socializing", "D": "Creative hobbies"},
    6: {"R": "Red", "B": "Black"},
    7: {"A": "Introverted", "B": "Extroverted"},
    8: {"A": "Love new experiences", "B": "Sometimes", "C": "Rarely"},
    9: {"R": "Red", "B": "Black"},
    10: {"A": "Analytical", "B": "Creative", "C": "Balanced"},
    11: {"A": "Alone", "B": "Team"},
    12: {"R": "Red", "B": "Black"},
    13: {"A": "Spontaneous", "B": "Planned"},
    14: {"A": "Often", "B": "Sometimes", "C": "Rarely"},
    15: {"R": "Red", "B": "Black"},
    16: {"A": "Yes", "B": "Sometimes", "C": "Not much"},
    17: {"A": "Very", "B": "Somewhat", "C": "Not important"},
    18: {"R": "Red", "B": "Black"},
    19: {"A": "Quickly", "B": "After thought"},
    20: {"A": "Success", "B": "Happiness", "C": "Growth", "D": "Peace"}
}

# ---------------------- ANALYZE PERSONALITY ----------------------
def analyze_personality(answers):
    red_count = sum(1 for q in answers if answers[q] == "R")
    black_count = sum(1 for q in answers if answers[q] == "B")

    traits = []
    if red_count > black_count:
        traits.append("bold")
    elif black_count > red_count:
        traits.append("calm")
    else:
        traits.append("balanced")

    if answers.get(7) == "A":
        traits.append("introspective")
    if answers.get(8) == "A":
        traits.append("curious")
    if answers.get(13) == "A":
        traits.append("spontaneous")
    if answers.get(14) == "A":
        traits.append("goal-oriented")

    if "bold" in traits and "curious" in traits:
        personality = "Explorer"
    elif "calm" in traits and "goal-oriented" in traits:
        personality = "Strategist"
    elif "spontaneous" in traits and "curious" in traits:
        personality = "Adventurer"
    else:
        personality = "Observer"

    description = f"You are a {personality}! This means you're {', '.join(traits)}."
    return personality, description

# ---------------------- CERTIFICATE ----------------------
def generate_certificate(name, personality, description):
    width, height = 900, 600
    background_color = (255, 248, 220)  # light cream
    border_color = (255, 69, 0)  # orange-red
    border_thickness = 20

    image = Image.new("RGB", (width, height), background_color)
    draw = ImageDraw.Draw(image)

    # Draw border
    for i in range(border_thickness):
        draw.rectangle(
            [i, i, width - i - 1, height - i - 1],
            outline=border_color
        )

    # Load fonts with fallback
    try:
        title_font = ImageFont.truetype("arial.ttf", 50)
        subtitle_font = ImageFont.truetype("arial.ttf", 28)
        body_font = ImageFont.truetype("arial.ttf", 22)
    except:
        title_font = ImageFont.load_default()
        subtitle_font = ImageFont.load_default()
        body_font = ImageFont.load_default()

    # Title
    title_text = "Certificate of Personality"
    bbox = draw.textbbox((0,0), title_text, font=title_font)
    w = bbox[2] - bbox[0]
    h = bbox[3] - bbox[1]
    draw.text(((width - w) / 2, 60), title_text, fill=border_color, font=title_font)

    # Recipient
    name_text = f"Presented to: {name}"
    bbox = draw.textbbox((0,0), name_text, font=subtitle_font)
    w = bbox[2] - bbox[0]
    h = bbox[3] - bbox[1]
    draw.text(((width - w) / 2, 160), name_text, fill="black", font=subtitle_font)

    # Personality
    personality_text = f"Personality Type: {personality}"
    bbox = draw.textbbox((0,0), personality_text, font=subtitle_font)
    w = bbox[2] - bbox[0]
    h = bbox[3] - bbox[1]
    draw.text(((width - w) / 2, 220), personality_text, fill="black", font=subtitle_font)

    # Description block (wrap text)
    def draw_multiline_text(draw_obj, text, pos, font, max_width, fill):
        lines = []
        words = text.split()
        line = ""
        for word in words:
            test_line = line + word + " "
            bbox = draw_obj.textbbox((0,0), test_line, font=font)
            w = bbox[2] - bbox[0]
            if w <= max_width:
                line = test_line
            else:
                lines.append(line)
                line = word + " "
        lines.append(line)

        y = pos[1]
        for line in lines:
            draw_obj.text((pos[0], y), line.strip(), font=font, fill=fill)
            bbox = draw_obj.textbbox((0,0), line.strip(), font=font)
            h = bbox[3] - bbox[1]
            y += h + 5

    description_text = description
    draw_multiline_text(draw, description_text, (70, 280), body_font, width - 140, fill="black")

    # Signature line
    sig_y = height - 100
    draw.line((width - 300, sig_y, width - 100, sig_y), fill=border_color, width=3)
    sig_text = "Signature"
    bbox = draw.textbbox((0,0), sig_text, font=body_font)
    w = bbox[2] - bbox[0]
    h = bbox[3] - bbox[1]
    draw.text((width - 200 - w / 2, sig_y + 10), sig_text, fill="black", font=body_font)

    return image
# ---------------------- UI & LOGIC ----------------------
st.title("🧠 Deep Personality Quiz")

if not st.session_state.username:
    st.session_state.username = st.text_input("Enter your name to start:")

if st.session_state.username:
    st.write(f"Welcome, **{st.session_state.username}**! Please answer the following questions:")

    # Show questions
    for q_num in sorted(questions.keys()):
        q_text = questions[q_num]
        opts = options[q_num]

        # Prepare options list for radio buttons
        option_keys = list(opts.keys())
        option_labels = [f"{key}: {opts[key]}" for key in option_keys]

        # Get current answer if any
        current_answer = st.session_state.answers.get(q_num, None)

        # Show radio with proper keys to maintain state
        selected_label = st.radio(
            label=q_text,
            options=option_labels,
            index=option_keys.index(current_answer) if current_answer in option_keys else 0,
            key=f"q{q_num}"
        )

        # Extract selected key from label (e.g. "A: Male" -> "A")
        selected_key = selected_label.split(":")[0]
        st.session_state.answers[q_num] = selected_key

    # Check if all questions answered
    all_answered = len(st.session_state.answers) == len(questions)
    if all_answered:
        if st.button("Submit Quiz"):
            st.session_state.submitted = True
    else:
        st.info(f"Please answer all {len(questions)} questions before submitting.")

else:
    st.info("Please enter your name to begin the quiz.")
# ---------------------- RESULTS & CERTIFICATE ----------------------
if st.session_state.submitted:
    personality, description = analyze_personality(st.session_state.answers)

    st.header("Your Personality Result")
    st.markdown(f"### {personality}")
    st.write(description)

    # Generate certificate image
    cert_img = generate_certificate(st.session_state.username, personality, description)

    # Display certificate
    st.image(cert_img, caption="Your Personality Certificate", use_column_width=True)

    # Prepare for download
    buf = io.BytesIO()
    cert_img.save(buf, format="PNG")
    byte_im = buf.getvalue()

    st.download_button(
        label="Download Certificate",
        data=byte_im,
        file_name=f"{st.session_state.username}_personality_certificate.png",
        mime="image/png"
    )
