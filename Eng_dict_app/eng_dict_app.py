# Function to update the timer
def update_timer():
    if st.session_state.get("timer_active", False):
        elapsed = datetime.now() - st.session_state.timer_start
        timer_placeholder.markdown(f"⏳ Time elapsed: {elapsed}")

# Initialize session state variables if they don't exist
if 'timer_active' not in st.session_state:
    st.session_state.timer_active = False
if 'timer_start' not in st.session_state:
    st.session_state.timer_start = datetime.now()
if 'question_number' not in st.session_state:
    st.session_state.question_number = 0
if 'score' not in st.session_state:
    st.session_state.score = {"right": 0, "close": 0, "incorrect": 0}
if 'incorrect_answers' not in st.session_state:
    st.session_state.incorrect_answers = []
if 'quiz_completed' not in st.session_state:
    st.session_state.quiz_completed = False

# Placeholder for the timer display
timer_placeholder = st.empty()

# Button to start the quiz and timer
if not st.session_state.timer_active:
    if st.button("Start Quiz (With Time)"):
        st.session_state.timer_start = datetime.now()
        st.session_state.timer_active = True

# Display questions and handle responses only if the quiz has started
if st.session_state.timer_active:
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
        
# Function to update the timer
def update_timer():
    if st.session_state.get("timer_active", False):
        elapsed = datetime.now() - st.session_state.timer_start
        timer_placeholder.markdown(f"⏳ Time elapsed: {elapsed}")

# Initialize session state variables if they don't exist
if 'timer_active' not in st.session_state:
    st.session_state.timer_active = False
if 'timer_start' not in st.session_state:
    st.session_state.timer_start = datetime.now()
if 'question_number' not in st.session_state:
    st.session_state.question_number = 0
if 'score' not in st.session_state:
    st.session_state.score = {"right": 0, "close": 0, "incorrect": 0}
if 'incorrect_answers' not in st.session_state:
    st.session_state.incorrect_answers = []
if 'quiz_completed' not in st.session_state:
    st.session_state.quiz_completed = False

# Placeholder for the timer display
timer_placeholder = st.empty()

# Button to start the quiz and timer
if not st.session_state.timer_active:
    if st.button("Start Quiz (With Time)"):
        st.session_state.timer_start = datetime.now()
        st.session_state.timer_active = True

# Display questions and handle responses only if the quiz has started
if st.session_state.timer_active:
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

    # Timer update loop, runs on every rerun
    update_timer()

    # Option to restart the quiz
    if st.session_state.get("quiz_completed", False):
        if st.button("Restart Quiz"):
            timer_placeholder.empty()  # Clear the final time display
            st.session_state.clear()  # Reset the session statez

