import streamlit as st
import pandas as pd
import re
import random

# Specify the URL to your PDF file
df = pd.read_excel('https://raw.githubusercontent.com/heydar432/Streamlit/main/Eng_dict_app/pdf_eng_words.xlsx')

df1 = df.copy()
# Display the resized image aligned to the center horizontally using CSS styling
st.markdown(
    f'<div style="display: flex; justify-content: center;"><img src="https://images-wixmp-ed30a86b8c4ca887773594c2.wixmp.com/f/087cab2d-fdd1-4960-96d4-99b8e6587e97/dgovrr-f7618dc4-6e94-4ce1-8bb7-6023cdeb4da1.jpg?token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJ1cm46YXBwOjdlMGQxODg5ODIyNjQzNzNhNWYwZDQxNWVhMGQyNmUwIiwiaXNzIjoidXJuOmFwcDo3ZTBkMTg4OTgyMjY0MzczYTVmMGQ0MTVlYTBkMjZlMCIsIm9iaiI6W1t7InBhdGgiOiJcL2ZcLzA4N2NhYjJkLWZkZDEtNDk2MC05NmQ0LTk5YjhlNjU4N2U5N1wvZGdvdnJyLWY3NjE4ZGM0LTZlOTQtNGNlMS04YmI3LTYwMjNjZGViNGRhMS5qcGcifV1dLCJhdWQiOlsidXJuOnNlcnZpY2U6ZmlsZS5kb3dubG9hZCJdfQ._pUfJfXa6QbLKihXmEVpkhycCB6mNLdTsWhoaDfdoDg" style="width: 200px;"></div>',
    unsafe_allow_html=True
)

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

# Add a radio button to choose the dataset
dataset_choice = st.radio(
    "Choose the dataset you want to use:",
    ('uşaqlar_1', 'Heydar_mixed_eng', '799_words', '54_words')
)

# Use the chosen dataset for the quiz
if dataset_choice == 'uşaqlar_1':
    df = df1  # Assuming df is your DataFrame for 'uşaqlar_1'
elif dataset_choice == 'Heydar_mixed_eng':
    df = pd.read_excel('https://raw.githubusercontent.com/heydar432/Streamlit/main/Eng_dict_app/Heydar_mixed_eng.xlsx')
elif dataset_choice == '799_words':
    df = pd.read_excel('https://raw.githubusercontent.com/heydar432/Streamlit/main/Eng_dict_app/799_words.xlsx')
else:
    df = pd.read_excel('https://raw.githubusercontent.com/heydar432/Streamlit/main/Eng_dict_app/54_words.xlsx')
    
# Inputs for start and end indexes, and number of questions

start_index = st.number_input("Choose start index for questions:", min_value=0, max_value=len(df)-1, value=0, key="start_index")
end_index = st.number_input("Choose end index for questions:", min_value=start_index, max_value=len(df)-1, value=min(start_index + 26, len(df)-1), key="end_index")
max_questions = end_index - start_index + 1
num_questions = st.number_input("How many questions do you want to answer?", min_value=1, max_value=max_questions, value=min(5, max_questions), key="num_questions")

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

# Display questions and handle responses
if st.session_state.question_number < len(st.session_state.random_indices):
    index = st.session_state.random_indices[st.session_state.question_number]
    term, correct_definitions, correct_pronounce = ask_question(index)
    st.write(f"Question {st.session_state.question_number + 1} of {len(st.session_state.random_indices)}")

    # Increased font size for the question
    st.markdown(f"<h3 style='text-align: center; color: light blue ;'>What is the definition or pronunciation of '{term}'?</h3>", unsafe_allow_html=True)
    
    user_answer = st.text_input("Your answer", key=f"user_answer_{st.session_state.question_number}")

    if st.button("Submit Answer", key=f"submit_{st.session_state.question_number}"):
        result, defs, pron = check_answer(user_answer, correct_definitions, correct_pronounce)
        if result == "right":
            st.success(f"Correct! Definition: '{defs}', Pronunciation: '{pron}'.")
            st.session_state.score["right"] += 1
        elif result == "close":
            st.warning(f"Close! Correct Definition: '{defs}', Pronunciation: '{pron}'.")
            st.session_state.score["close"] += 1
        else:
            st.error(f"Incorrect. The correct Definition is '{defs}', and the Pronunciation is '{pron}'.")
            st.session_state.score["incorrect"] += 1
            # Store the incorrect answer along with its definition and pronunciation
            st.session_state.incorrect_answers.append((term, defs, pron))

        st.session_state.question_number += 1
else:
    st.markdown(f"<h3 style='text-align: left; color: green;'>Quiz Completed!</h3>", unsafe_allow_html=True)
    st.markdown(f"<span style='font-size: 18px;'>Quiz Results:</span>", unsafe_allow_html=True)
    st.markdown(f"<span style='font-size: 18px;'>Right answers: {st.session_state.score['right']}</span>", unsafe_allow_html=True)
    st.markdown(f"<span style='font-size: 18px;'>Close answers: {st.session_state.score['close']}</span>", unsafe_allow_html=True)
    st.markdown(f"<span style='font-size: 18px;'>Incorrect answers: {st.session_state.score['incorrect']}</span>", unsafe_allow_html=True)


    if st.session_state.incorrect_answers:
        st.markdown("<h2 style='text-align: center; color: red;'>Review the incorrect answers:</h2>", unsafe_allow_html=True)
        for term, defs, pron in st.session_state.incorrect_answers:
            # "Term" and {term} are bold and in default size for <h4>
            st.markdown(f"<h4 style='text-align: left; color: black; font-weight: bold;'>Term: <span style='color: red;'>{term}</span></h4>", unsafe_allow_html=True)
            
            # "Definition", "Pronunciation", and their contents are just slightly smaller, at 14px
            st.markdown(f"<h4 style='text-align: left; color: black; font-size: 20px;'>Definition: <span style='color: red; font-style: italic;'>{defs}</span></h4>", unsafe_allow_html=True)
            st.markdown(f"<h4 style='text-align: left; color: black; font-size: 20px;'>Pronunciation: <span style='color: red; font-style: italic;'>{pron}</span></h4>", unsafe_allow_html=True)


    # Option to restart the quiz
    if st.button("Restart Quiz"):
        st.session_state.clear()
