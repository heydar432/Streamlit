import streamlit as st
import pandas as pd
import re
import random
import SpeechRecognition as sr

# Load the DataFrame with st.cache_data
@st.cache(allow_output_mutation=True)
def load_data():
    return pd.read_excel('https://raw.githubusercontent.com/heydar432/Streamlit/main/Eng_dict_app/pdf_eng_words.xlsx')

df = load_data()

# Function to clean strings
def clean_string(input_string):
    normalized_string = input_string.replace('-', ' ').lower()
    cleaned_string = re.sub(r'[^a-zA-Z0-9\s]', '', normalized_string).strip()
    return cleaned_string

# Speech Recognition Function
def transcribe_audio(audio_file):
    recognizer = sr.Recognizer()
    with sr.AudioFile(audio_file) as source:
        audio_data = recognizer.record(source)
        try:
            text = recognizer.recognize_google(audio_data, language='en-EN')
            return text
        except sr.UnknownValueError:
            return "Speech Recognition could not understand the audio"
        except sr.RequestError as e:
            return f"Could not request results; {e}"

# Other functions (is_close_enough, ask_question, check_answer) remain the same

# Streamlit UI
st.title("Lancocraft Language Learning Quiz")

# Inputs for start and end indexes, and number of questions
start_index, end_index, num_questions = 0, len(df)-1, 5  # Simplified for demonstration

# Display questions and handle responses
index = random.randint(start_index, end_index)
term, correct_definitions, correct_pronounce = ask_question(index)

st.write(f"What is the definition or pronunciation of '{term}'?")

# Option to input answer as text or upload audio file
answer_mode = st.radio("Select your answer mode:", ('Type', 'Speak'))

# Option to input answer as text or upload audio file
answer_mode = st.radio("Select your answer mode:", ('Type', 'Speak'))

if answer_mode == 'Type':
    user_answer = st.text_input("Type your answer here:")
else:
    audio_file = st.file_uploader("Upload your spoken answer as an audio file:", type=['wav', 'mp3'])
    if audio_file is not None:
        user_answer = transcribe_audio(audio_file)
        st.write(f"Transcribed Text: {user_answer}")
    else:
        user_answer = ""

if st.button("Submit Answer"):
    if user_answer:
        result, defs, pron = check_answer(user_answer, correct_definitions, correct_pronounce)
        if result == "right":
            st.success(f"Correct! Definition: '{defs}', Pronunciation: '{pron}'.")
        elif result == "close":
            st.warning(f"Close! Correct Definition: '{defs}', Pronunciation: '{pron}'.")
        else:
            st.error(f"Incorrect. The correct Definition is '{defs}', and the Pronunciation is '{pron}'.")
    else:
        st.error("Please enter an answer or upload an audio file.")
