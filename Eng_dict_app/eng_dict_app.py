import streamlit as st
import pandas as pd
import re
import random
from datetime import datetime
import time

# Initialize session state variables for the timer if they don't exist
if 'timer_start' not in st.session_state:
    st.session_state.timer_start = None

if 'timer_active' not in st.session_state:
    st.session_state.timer_active = False

# Function to display and update the timer
def update_timer():
    if st.session_state.timer_start and st.session_state.timer_active:
        # Calculate elapsed time
        elapsed = datetime.now() - st.session_state.timer_start
        # Display the timer
        timer_placeholder.markdown(f"<h3 style='text-align: center;'>Time: {str(elapsed).split('.')[0]}</h3>", unsafe_allow_html=True)

# Timer display placeholder
timer_placeholder = st.empty()

# Function to clean strings
def clean_string(input_string):
    normalized_string = input_string.replace('-', ' ').lower()
    cleaned_string = re.sub(r'[^a-zA-Z0-9\s]', '', normalized_string).strip()
    return cleaned_string

# Function to check if an answer is close enough
def is_close_enough(user_answer, correct_answers):
    user_answer_cleaned = clean_string(user_answer)
    possible_answers = [clean_string(answer) for answer in correct_answers.split(',')]
    is_close = False
    is_exact = False

    for correct_answer in possible_answers:
        user_answer_no_spaces = user_answer_cleaned.replace(' ', '')
        correct_answer_no_spaces = correct_answer.replace(' ', '')
        if user_answer_no_spaces == correct_answer_no_spaces:
            is_exact = True
            break
        elif len(correct_answer_no_spaces) > 4:
            diff_count = sum(1 for a, b in zip(user_answer_no_spaces, correct_answer_no_spaces) if a != b)
            diff_count += abs(len(user_answer_no_spaces) - len(correct_answer_no_spaces))
            if diff_count <= 1:
                is_close = True
    return is_close, is_exact

# Function to ask a question based on the random indices
def ask_question(index):
    random_row = df.iloc[index]
    term = random_row['Term']
    correct_definitions = random_row['Definition']
    correct_pronounce = random_row['Pronounce']
    return term, correct_definitions, correct_pronounce

# Function to check the user's answer
def check_answer(user_answer, correct_definitions, correct_pronounce):
    is_close, is_exact = is_close_enough(user_answer, correct_definitions)
    if user_answer == correct_pronounce.lower() or is_exact:
        return "right", correct_definitions, correct_pronounce
    elif is_close:
        return "close", correct_definitions, correct_pronounce
    else:
        return "incorrect", correct_definitions, correct_pronounce

# Streamlit UI
st.markdown("<h1 style='text-align: center; color: violet;'>Lancocraft Language Learning Quiz</h1>", unsafe_allow_html=True)

# Load the initial data
df = pd.read_excel('https://raw.githubusercontent.com/heydar432/Streamlit/main/Eng_dict_app/pdf_eng_words.xlsx')
df1 = df.copy()

# Add a radio button to choose the dataset
dataset_choice = st.radio(
    "Choose the dataset you want to use:",
    ('uşaqlar_1', 'Heydar_mixed_eng', '799_words', '54_words')
)

# Use the chosen dataset for the quiz
if dataset_choice == 'uşaqlar_1':
    df = df1  # Assuming df1 is your DataFrame for 'uşaqlar_1'
elif dataset_choice == 'Heydar_mixed_eng':
    # Convert Google Sheets URL to a CSV export format for 'Heydar_mixed_eng'
    heydar_sheet_id = '1SxNKWXeXQzE2WHj1sQ_sMRO5KqW6Jb-y'
    heydar_sheet_name = 'Sheet1'  # Replace with the actual sheet name if different
    heydar_google_sheet_url = f'https://docs.google.com/spreadsheets/d/{heydar_sheet_id}/gviz/tq?tqx=out:csv&sheet={heydar_sheet_name}'
    df = pd.read_csv(heydar_google_sheet_url)
elif dataset_choice == '799_words':
    # Convert Google Sheets URL to a CSV export format for '799_words'
    words_799_sheet_id = '15ByeHMRtCroYD1zN2Tymlecq5A-xHPE-'
    words_799_sheet_name = 'Sheet1'  # Replace with the actual sheet name if different
    words_799_google_sheet_url = f'https://docs.google.com/spreadsheets/d/{words_799_sheet_id}/gviz/tq?tqx=out:csv&sheet={words_799_sheet_name}'
    df = pd.read_csv(words_799_google_sheet_url)
else:
    # Convert Google Sheets URL to a CSV export format for '54_words'
    words_54_sheet_id = '1u7howTZIMTL9REa7SIX3-J3i73bIABSH'
    words_54_sheet_name = 'Sheet1'  # Replace with the actual sheet name if different
    words_54_google_sheet_url = f'https://docs.google.com/spreadsheets/d/{words_54_sheet_id}/gviz/tq?tqx=out:csv&sheet={words_54_sheet_name}'
    df = pd.read_csv(words_54_google_sheet_url)

# Inputs for start and end indexes, and number of questions
start_index = st.number_input("Choose start index for questions:", min_value=0, max_value=len(df)-1, value=0, step=1)
end_index = st.number_input("Choose end index for questions:", min_value=0, max_value=len(df)-1, value=len(df)-1, step=1)
num_questions = st.number_input("How many questions do you want to answer?", min_value=1, max_value=end_index-start_index+1, value=5, step=1)

# Generate random indices for questions if not already done
if 'random_indices' not in st.session_state or len(st.session_state.random_indices) != num_questions:
    st.session_state.random_indices = random.sample(range(start_index, end_index + 1), num_questions)

# Initialize scores, question number, and incorrect answers list if not already initialized
if 'score' not in st.session_state:
    st.session_state.score = {"right": 0, "close": 0, "incorrect": 0}
if 'question_number' not in st.session_state:
    st.session_state.question_number = 0
if 'incorrect_answers' not in st.session_state:
    st.session_state.incorrect_answers = []

# Button to start the quiz and timer
if not st.session_state.timer_active:
    if st.button("Start Quiz"):
        st.session_state.timer_start = datetime.now()
        st.session_state.timer_active = True

# Display questions and handle responses
if st.session_state.question_number < len(st.session_state.random_indices):
    index = st.session_state.random_indices[st.session_state.question_number]
    term, correct_definitions, correct_pronounce = ask_question(index)
    st.write(f"Question {st.session_state.question_number + 1} of {len(st.session_state.random_indices)}")

    user_answer = st.text_input("Your answer", key=f"user_answer_{st.session_state.question_number}")

    if st.button("Submit Answer", key=f"submit_{st.session_state.question_number}"):
        result, defs, pron = check_answer(user_answer, correct_definitions, correct_pronounce)
        if result == "right":
            st.success(f"Correct! The definition is '{defs}' and pronunciation is '{pron}'.")
            st.session_state.score["right"] += 1
        elif result == "close":
            st.warning(f"Close! The definition is '{defs}' and pronunciation is '{pron}'.")
            st.session_state.score["close"] += 1
        else:
            st.error(f"Incorrect. The definition is '{defs}' and pronunciation is '{pron}'.")
            st.session_state.score["incorrect"] += 1
            st.session_state.incorrect_answers.append((term, defs, pron, user_answer))

        st.session_state.question_number += 1
else:
    st.markdown("<h2 style='text-align: center; color: green;'>Quiz Completed!</h2>", unsafe_allow_html=True)

    # Display quiz results
    st.write(f"Right answers: {st.session_state.score['right']}")
    st.write(f"Close answers: {st.session_state.score['close']}")
    st.write(f"Incorrect answers: {st.session_state.score['incorrect']}")

    if st.session_state.incorrect_answers:
        st.markdown("<h2 style='text-align: center; color: red;'>Review the incorrect answers:</h2>", unsafe_allow_html=True)
        for term, defs, pron, user_ans in st.session_state.incorrect_answers:
            st.markdown(f"<h4 style='text-align: left; color: black; font-weight: bold;'>Term: <span style='color: red;'>{term}</span></h4>", unsafe_allow_html=True)
            
            # Use a placeholder text if user_ans is empty or None
            user_ans_display = user_ans if user_ans else '---'
            st.markdown(f"<h4 style='text-align: left; color: black; font-size: 18px;'> ✍️❌  <span style='color: blue;'>'{user_ans_display}'</span></h4>", unsafe_allow_html=True)
            st.markdown(f"<h4 style='text-align: left; color: black; font-size: 20px;'> 📖✔️ <span style='color: red; font-style: italic;'>{defs}</span></h4>", unsafe_allow_html=True)
            st.markdown(f"<h4 style='text-align: left; color: black; font-size: 20px;'> 📣✔️ <span style='color: red; font-style: italic;'> [ {pron} ]</span></h4>", unsafe_allow_html=True)

    # Option to restart the quiz
    if st.button("Restart Quiz"):
        st.session_state.clear()

# Timer update loop, runs on every rerun
update_timer()
