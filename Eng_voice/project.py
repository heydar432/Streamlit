import streamlit as st
import pandas as pd
import re
import random
from datetime import datetime
import time

# Display the resized image aligned to the center horizontally using CSS styling
st.markdown(
    f'<div style="display: flex; justify-content: center;"><img src="https://images-wixmp-ed30a86b8c4ca887773594c2.wixmp.com/f/087cab2d-fdd1-4960-96d4-99b8e6587e97/dgovrr-f7618dc4-6e94-4ce1-8bb7-6023cdeb4da1.jpg?token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJ1cm46YXBwOjdlMGQxODg5ODIyNjQzNzNhNWYwZDQxNWVhMGQyNmUwIiwiaXNzIjoidXJuOmFwcDo3ZTBkMTg4OTgyMjY0MzczYTVmMGQ0MTVlYTBkMjZlMCIsIm9iaiI6W1t7InBhdGgiOiJcL2ZcLzA4N2NhYjJkLWZkZDEtNDk2MC05NmQ0LTk5YjhlNjU4N2U5N1wvZGdvdnJyLWY3NjE4ZGM0LTZlOTQtNGNlMS04YmI3LTYwMjNjZGViNGRhMS5qcGcifV1dLCJhdWQiOlsidXJuOnNlcnZpY2U6ZmlsZS5kb3dubG9hZCJdfQ._pUfJfXa6QbLKihXmEVpkhycCB6mNLdTsWhoaDfdoDg" style="width: 200px;"></div>',
    unsafe_allow_html=True
)

# Streamlit UI
st.markdown("<h1 style='text-align: center; color: violet;'>Lancocraft Language Learning Quiz 2</h1>", unsafe_allow_html=True)

# Add a radio button to choose the dataset
dataset_choice = st.radio(
    "Choose the dataset you want to use:",
    ('uşaqlar_1', 'Heydar_mixed_eng', '799_words', '54_words')
)

# Mapping of dataset choices to their respective Google Sheet IDs and Sheet names
datasets = {
    'uşaqlar_1': ('1MvSa70n992Fs0jmS1vEjux4x4NzT6KaO', 'Sheet1'),
    'Heydar_mixed_eng': ('1SxNKWXeXQzE2WHj1sQ_sMRO5KqW6Jb-y', 'Sheet1'),
    '799_words': ('15ByeHMRtCroYD1zN2Tymlecq5A-xHPE-', 'Sheet1'),
    '54_words': ('1u7howTZIMTL9REa7SIX3-J3i73bIABSH', 'Sheet1'),
}

# Use the chosen dataset for the quiz
sheet_id, sheet_name = datasets[dataset_choice]
google_sheet_url = f'https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}'
df = pd.read_csv(google_sheet_url)



# Function to clean strings
def clean_string(input_string):
    normalized_string = input_string.replace('-', ' ').lower()
    cleaned_string = re.sub(r'[^a-zA-Z0-9\s]', '', normalized_string).strip()
    return cleaned_string

def is_close_enough(user_answer, correct_answers):
    user_answer_cleaned = clean_string(user_answer)
    possible_answers = [clean_string(answer) for answer in correct_answers.split(',')]
    is_close = False
    is_exact = False

    for correct_answer in possible_answers:
        # Check for exact match
        if user_answer_cleaned == correct_answer:
            is_exact = True
            break

        # Ensure the user's answer has more than 4 letters before proceeding
        if len(user_answer_cleaned) > 4:
            # Condition 1: Check if the user's answer is incorrect by only one letter
            if len(user_answer_cleaned) == len(correct_answer):
                diff_count = sum(1 for a, b in zip(user_answer_cleaned, correct_answer) if a != b)
                if diff_count == 1:
                    is_close = True
                    break

            # Condition 2: Check if the user's answer has one more or one less letter, with remaining letters being the same
            elif abs(len(user_answer_cleaned) - len(correct_answer)) == 1:
                # Longer user answer case
                if len(user_answer_cleaned) > len(correct_answer):
                    shorter, longer = correct_answer, user_answer_cleaned
                else:
                    shorter, longer = user_answer_cleaned, correct_answer

                # Check if the shorter string is a substring of the longer, with one extra character in the longer string
                for i in range(len(longer)):
                    if shorter == longer[:i] + longer[i+1:]:
                        is_close = True
                        break
                if is_close:
                    break

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


# Inputs for start and end indexes, and number of questions

st.markdown("""
    <style>
    .start-index-desc, .end-index-desc, .num-questions-desc { 
        font-weight: bold; 
        font-size: 16px; 
        margin-bottom: 0px; /* Reduces space below the title */
    }
    .stNumberInput > div { 
        margin-top: 0px; /* Reduces space above the number input widget */
    }
    </style>
    <p class="start-index-desc">Choose start index for questions:</p>
    """, unsafe_allow_html=True)

start_index = st.number_input("", min_value=0, max_value=len(df)-1, value=0, key="start_index")

# No need for separate markdown for end_index, CSS already defined
st.markdown("<p class='end-index-desc'>Choose end index for questions:</p>", unsafe_allow_html=True)
end_index = st.number_input("", min_value=start_index, max_value=len(df)-1, value=min(start_index + 26, len(df)-1), key="end_index")

max_questions = end_index - start_index + 1

# No need for separate markdown for num_questions, CSS already defined
st.markdown("<p class='num-questions-desc'>How many questions do you want to answer?</p>", unsafe_allow_html=True)
num_questions = st.number_input("", min_value=1, max_value=max_questions, value=min(5, max_questions), key="num_questions")

# Initialize session state variables for the timer if they don't exist
if 'timer_start' not in st.session_state:
    st.session_state.timer_start = None

if 'timer_active' not in st.session_state:
    st.session_state.timer_active = False


# Function to display and update the timer
def update_timer():
    # Ensure 'timer_start' and 'timer_active' are initialized in session_state
    if 'timer_start' not in st.session_state:
        st.session_state.timer_start = None
    if 'timer_active' not in st.session_state:
        st.session_state.timer_active = False

    # Now it's safe to check the conditions
    if st.session_state.timer_start and st.session_state.timer_active:
        # Calculate elapsed time
        elapsed = datetime.now() - st.session_state.timer_start
        # Display the timer
        timer_placeholder.markdown(f"<h3 style='text-align: center;'>Time: {str(elapsed).split('.')[0]}</h3>", unsafe_allow_html=True)

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
    if st.button("Start Quiz (With Time)"):
        st.session_state.timer_start = datetime.now()
        st.session_state.timer_active = True

# Timer display placeholder
timer_placeholder = st.empty()

# Display questions and handle responses
if st.session_state.question_number < len(st.session_state.random_indices):
    index = st.session_state.random_indices[st.session_state.question_number]
    term, correct_definitions, correct_pronounce = ask_question(index)
    st.write(f"Question {st.session_state.question_number + 1} of {len(st.session_state.random_indices)}")

    # Increased font size for the question
    st.markdown(f"""
        <h3 style='text-align: center; color: brown;'>
            <span style='font-size: smaller;'>What is the definition or pronunciation of</span>
            <span style='font-weight: bold; font-style: italic;'> '{term}'</span>?
        </h3>
        """, unsafe_allow_html=True)
        
    user_answer = st.text_input("Your answer", key=f"user_answer_{st.session_state.question_number}")

    if st.button("Submit Answer", key=f"submit_{st.session_state.question_number}"):
        result, defs, pron = check_answer(user_answer, correct_definitions, correct_pronounce)
        if result == "right":
            st.success(f" ✅ Correct! The correct 📖✔️ '{defs}', 📣✔️ '{pron}'.")
            st.session_state.score["right"] += 1
        elif result == "close":
            st.warning(f" ⚠️ Close! The correct 📖✔️ '{defs}', 📣✔️ '{pron}'.")
            st.session_state.score["close"] += 1
        else:
            st.error(f" ❌ Incorrect. The correct 📖✔️ '{defs}', 📣✔️ '{pron}'.")
            st.session_state.score["incorrect"] += 1
            st.session_state.incorrect_answers.append((term, defs, pron, user_answer))

        st.session_state.question_number += 1
else: 
    # After the last question is answered and the quiz is completed:
    if not st.session_state.get("quiz_completed", False):  # Check if this hasn't been set yet
        st.session_state.quiz_completed = True  # Mark the quiz as completed to stop the timer
        
    st.markdown(f"<h3 style='text-align: center; color: green;'>Quiz Completed!</h3>", unsafe_allow_html=True)
    # Display quiz results and potentially incorrect answers here
    st.markdown(f"<span style='font-size: 18px; font-weight: bold;'> 📊 Quiz Results:</span>", unsafe_allow_html=True)
    st.markdown(f"<span style='font-size: 18px; font-weight: bold;'> ✅ Right answers: {st.session_state.score['right']}</span>", unsafe_allow_html=True)
    st.markdown(f"<span style='font-size: 18px; font-weight: bold;'> ⚠️ Close answers: {st.session_state.score['close']}</span>", unsafe_allow_html=True)
    st.markdown(f"<span style='font-size: 18px; font-weight: bold;'> ❌ Incorrect answers: {st.session_state.score['incorrect']}</span>", unsafe_allow_html=True)

    if st.session_state.incorrect_answers:
        st.markdown("<h2 style='text-align: center; color: red;'>Review the incorrect answers:</h2>", unsafe_allow_html=True)
        for term, defs, pron, user_ans in st.session_state.incorrect_answers:
            st.markdown(f"<h4 style='text-align: left; color: black; font-weight: bold;'>Term: <span style='color: red;'>{term}</span></h4>", unsafe_allow_html=True)
            
            # Use a placeholder text if user_ans is empty or None
            user_ans_display = user_ans if user_ans else '---'
            st.markdown(f"<h4 style='text-align: left; color: black; font-size: 18px;'> ✍️❌  <span style='color: blue;'>'{user_ans_display}'</span></h4>", unsafe_allow_html=True)
            st.markdown(f"<h4 style='text-align: left; color: black; font-size: 20px;'> 📖✔️ <span style='color: black; font-style: italic;'>{defs}</span></h4>", unsafe_allow_html=True)
            st.markdown(f"<h4 style='text-align: left; color: black; font-size: 20px;'> 📣✔️ <span style='color: black; font-style: italic;'> [ {pron} ]</span></h4>", unsafe_allow_html=True)

# Option to restart the quiz
if st.session_state.get("quiz_completed", False):
    if st.button("Restart Quiz"):
        timer_placeholder.empty()  # Clear the final time display
        st.session_state.clear()  # Reset the session statez

# Timer update loop, runs on every rerun
update_timer()
