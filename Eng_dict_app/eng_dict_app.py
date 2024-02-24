import streamlit as st
import pandas as pd
import re

# Load the DataFrame
df = pd.read_excel('https://raw.githubusercontent.com/heydar432/Streamlit/main/Eng_dict_app/pdf_eng_words.xlsx')

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

def ask_question(index):
    if index < len(df):
        random_row = df.iloc[index]
        term = random_row['Term']
        correct_definitions = random_row['Definition']
        correct_pronounce = random_row['Pronounce']
        return term, correct_definitions, correct_pronounce
    return None, None, None

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

# User selects the range of words
start_index, end_index = st.slider("Select the range of questions:", 0, len(df)-1, (0, 5), 1)
question_range = range(start_index, end_index + 1)

# Initialize session state variables if they don't exist
if 'score' not in st.session_state:
    st.session_state.score = {"right": 0, "close": 0, "incorrect": 0}
if 'current_index' not in st.session_state:
    st.session_state.current_index = 0
if 'range' not in st.session_state:
    st.session_state.range = (0, len(df) - 1)

# Set the title of the app
st.title("Language Learning Quiz")

# Slider for selecting the range of questions
min_question, max_question = st.slider('Select the range of questions:',
                                       0, len(df) - 1, (0, len(df) - 1))
st.session_state.range = (min_question, max_question)

question_count = 5  # Total number of questions to ask

# Ask questions within the selected range
if st.session_state.current_index < question_count:
    if 'current_question' not in st.session_state:
        # Randomly select a question within the range
        random_index = random.randint(st.session_state.range[0], st.session_state.range[1])
        random_row = df.iloc[random_index]
        st.session_state.current_question = {"term": random_row['Term'],
                                             "definitions": random_row['Definition'],
                                             "pronounce": random_row['Pronounce']}

    # Show the current question number and term
    st.write(f"Question {st.session_state.current_index + 1} of {question_count}")
    st.write(f"What is the definition or pronounce of '{st.session_state.current_question['term']}'?")

    # Input for the user's answer
    user_answer = st.text_input("Your answer", key=f"user_answer_{st.session_state.current_index}")

    if st.button("Submit Answer", key=f"submit_{st.session_state.current_index}"):
        # Process the answer
        # ...

        # Prepare the next question
        st.session_state.current_index += 1
        del st.session_state['current_question']

else:
    st.write("Quiz Completed!")
    st.write("Quiz Results:")
    st.write(f"Right answers: {st.session_state.score['right']}")
    st.write(f"Close answers: {st.session_state.score['close']}")
    st.write(f"Incorrect answers: {st.session_state.score['incorrect']}")

    # Reset the quiz if needed
    if st.button("Restart quiz"):
        st.session_state.current_index = 0
        st.session_state.score = {"right": 0, "close": 0, "incorrect": 0}
        del st.session_state['current_question']
