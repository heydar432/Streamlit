import streamlit as st
import pandas as pd
import re
import random

# Load the DataFrame
df = pd.read_excel('https://raw.githubusercontent.com/heydar432/Streamlit/main/Eng_dict_app/pdf_eng_words.xlsx')

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

# Function to ask a question based on the question number
def ask_question(question_number):
    index = 459 + question_number  # Start from index 
    if index < len(df):
        random_row = df.iloc[index]
        term = random_row['Term']
        correct_definitions = random_row['Definition']
        correct_pronounce = random_row['Pronounce']
        return term, correct_definitions, correct_pronounce
    return None, None, None

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
st.title("Language Learning Quiz")

if 'score' not in st.session_state:
    st.session_state.score = {"right": 0, "close": 0, "incorrect": 0}

question_count = 27  # Total number of questions to ask

if 'question_number' not in st.session_state:
    st.session_state.question_number = 0

if st.session_state.question_number < question_count:
    term, correct_definitions, correct_pronounce = ask_question(st.session_state.question_number)
    if term is not None:
        st.write(f"Question {st.session_state.question_number + 1} of {question_count}")
        st.write(f"What is the definition or pronounce of '{term}'?")
        user_answer = st.text_input("Your answer", key=f"user_answer_{st.session_state.question_number}")

        if st.button("Submit Answer", key=f"submit_{st.session_state.question_number}"):
            result, defs, pron = check_answer(user_answer, correct_definitions, correct_pronounce)
            if result == "right":
                st.success(f"Your answer is right. One possible correct definition is '{defs}', and the pronounce is '{pron}'.")
                st.session_state.score["right"] += 1
            elif result == "close":
                st.warning(f"Your answer is close but not completely correct. One possible correct definition is '{defs}', and the pronounce is '{pron}'.")
                st.session_state.score["close"] += 1
            else:
                st.error(f"Your answer is not correct. One possible correct definition is '{defs}', and the pronounce is '{pron}'.")
                st.session_state.score["incorrect"] += 1

            st.session_state.question_number += 1
    else:
        st.error("No more questions available.")
else:
    st.write("Quiz Completed!")
    st.write("Quiz Results:")
    st.write(f"Right answers: {st.session_state.score['right']}")
    st.write(f"Close answers: {st.session_state.score['close']}")
    st.write(f"Incorrect answers: {st.session_state.score['incorrect']}")
