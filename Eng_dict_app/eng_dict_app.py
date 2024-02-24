import streamlit as st
import pandas as pd
import re

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

# Updated function to ask a question based on available questions
def ask_question(available_questions, df):
    if available_questions:
        question_number = random.choice(available_questions)  # Randomly select a question number
        available_questions.remove(question_number)  # Remove the selected question from the pool
        index = 459 + question_number  # Calculate index based on the selected question number
        if index < len(df):
            random_row = df.iloc[index]
            term = random_row['Term']
            correct_definitions = random_row['Definition']
            correct_pronounce = random_row['Pronounce']
            return term, correct_definitions, correct_pronounce, available_questions
    return None, None, None, available_questions

# Function to check the user's answer remains the same
def check_answer(user_answer, correct_definitions, correct_pronounce):
    is_close, is_exact = is_close_enough(user_answer, correct_definitions)
    if user_answer == correct_pronounce.lower() or is_exact:
        return "right", correct_definitions, correct_pronounce
    elif is_close:
        return "close", correct_definitions, correct_pronounce
    else:
        return "incorrect", correct_definitions, correct_pronounce

# Streamlit UI setup
st.title("Language Learning Quiz")

# Initialize session state variables
if 'score' not in st.session_state:
    st.session_state.score = {"right": 0, "close": 0, "incorrect": 0}

if 'available_questions' not in st.session_state:
    st.session_state.available_questions = list(range(27))  # Initialize with a list of question numbers

# Main quiz functionality
if st.session_state.available_questions:
    term, correct_definitions, correct_pronounce, st.session_state.available_questions = ask_question(st.session_state.available_questions, df)
    if term is not None:
        question_display = len(st.session_state.score["right"]) + len(st.session_state.score["close"]) + len(st.session_state.score["incorrect"]) + 1
        st.write(f"Question {question_display} of 27")
        st.write(f"What is the definition or pronounce of '{term}'?")
        user_answer = st.text_input("Your answer", key=f"user_answer_{question_display}")

        if st.button("Submit Answer", key=f"submit_{question_display}"):
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
else:
    st.write("Quiz Completed!")
    st.write("Quiz Results:")
    st.write(f"Right answers: {st.session_state.score['right']}")
    st.write(f"Close answers: {st.session_state.score['close']}")
    st.write(f"Incorrect answers: {st.session_state.score['incorrect']}")
