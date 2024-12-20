import os
import streamlit as st
from pdf_extractor import extract_text_from_pdf
from quiz_handler import generate_quiz, evaluate_quiz
from db import save_quiz_result, get_student_quiz_results, get_all_quiz_results
from auth import has_role

UPLOAD_DIR = "uploaded_pdfs"

def quizzes():
    st.markdown("<h1 style='color: #4CAF50;'>Take a Quiz</h1>", unsafe_allow_html=True)

    # Retrieve user details from session state
    user = st.session_state.get("user")
    if not user:
        st.warning("You must be logged in to access this page.")
        return

    role = user["role"]
    student_id = user["id"]

    # Student View: Quiz Generation and History
    if role == "student":
        # Ensure there are uploaded PDFs
        pdf_files = [f for f in os.listdir(UPLOAD_DIR) if f.endswith(".pdf")]
        if not pdf_files:
            st.warning("No lecture materials available. Please upload course materials first.")
            return

        # Lecture Selection
        st.markdown("<h3 style='color: #362f2f; font-weight: bold;'>Select a Lecture to Generate a Quiz</h3>", unsafe_allow_html=True)
        selected_lecture = st.selectbox("Choose a Lecture:", pdf_files)

        # Difficulty Level Selection
        st.markdown("<h3 style='color: #362f2f; font-weight: bold;'>Choose Difficulty Level</h3>", unsafe_allow_html=True)
        difficulty = st.radio("Difficulty Level:", ["easy", "medium", "hard"])

        # Generate Quiz
        if st.button("Generate Quiz"):
            # Extract PDF content
            pdf_path = os.path.join(UPLOAD_DIR, selected_lecture)
            pdf_content = extract_text_from_pdf(pdf_path)

            if not pdf_content:
                st.error("Failed to extract content from the selected PDF.")
                return

            # Generate Quiz Questions and Answers
            st.info("Generating quiz based on course material... Please wait!")
            quiz_questions, correct_answers = generate_quiz(pdf_content, difficulty)
            st.session_state.quiz_questions = quiz_questions
            st.session_state.correct_answers = correct_answers
            st.session_state.selected_lecture = selected_lecture
            st.session_state.difficulty = difficulty
            st.session_state.submitted = False

        # Display Quiz Form
        if "quiz_questions" in st.session_state and not st.session_state.get("submitted", False):
            st.markdown("<h3 style='color: #362f2f; font-weight: bold;'>Quiz Form</h3>", unsafe_allow_html=True)
            submitted_answers = {}
            for idx, question in enumerate(st.session_state.quiz_questions):
                st.markdown(f"**Q{idx + 1}: {question['question']}**")
                if question["type"] == "mcq_single":
                    submitted_answers[idx] = st.radio("Choose:", question["options"], key=f"q{idx}")
                elif question["type"] == "true_false":
                    submitted_answers[idx] = st.radio("True/False:", question["options"], key=f"q{idx}")
                elif question["type"] == "mcq_multiple":
                    submitted_answers[idx] = st.multiselect("Select all:", question["options"], key=f"q{idx}")

            if st.button("Submit Quiz"):
                # Evaluate quiz
                score, total, feedback = evaluate_quiz(submitted_answers, st.session_state.correct_answers)
                st.session_state.submitted = True
                st.success(f"Quiz Submitted! Your Score: {score}/{total}")

                # Save quiz result
                save_quiz_result(student_id, st.session_state.selected_lecture,
                                 st.session_state.difficulty, score, total)
                st.session_state.feedback = feedback

        # Display Results
        if st.session_state.get("submitted", False):
            st.markdown("<h3 style='color: #362f2f; font-weight: bold;'>Quiz Results</h3>", unsafe_allow_html=True)
            for idx, result in st.session_state.feedback.items():
                st.write(f"Q{idx + 1}: {result}")

        # Display Quiz History
        st.markdown("<h3 style='color: #362f2f; font-weight: bold;'>Your Quiz Results</h3>", unsafe_allow_html=True)
        results = get_student_quiz_results(student_id)
        if not results:
            st.info("You have not taken any quizzes yet.")
        else:
            for result in results:
                st.write(f"**Lecture**: {result[0]}")
                st.write(f"**Difficulty**: {result[1]}")
                st.write(f"**Score**: {result[2]}/{result[3]}")
                st.write(f"**Date**: {result[4]}")
                st.write("---")

    # Teacher View: Show Only Student Results
    elif role == "teacher":
        st.markdown("<h3 style='color: #362f2f; font-weight: bold;'>All Students' Quiz Results</h3>", unsafe_allow_html=True)
        
        # Filter Section
        st.markdown("<h3 style='color: #362f2f; font-weight: bold;'>Filter by Student ID</h3>", unsafe_allow_html=True)
        student_id_filter = st.text_input("Enter Student ID (optional):")

        # Fetch all quiz results
        all_results = get_all_quiz_results()

        # Apply filter
        if student_id_filter:
            all_results = [r for r in all_results if str(r[0]) == student_id_filter]
            st.markdown("<h3 style='color: #362f2f; font-weight: bold;'>Showing Filtered Results for Student ID:</h3>", unsafe_allow_html=True)
        else:
            st.markdown("<h3 style='color: #362f2f; font-weight: bold;'>Showing All Quiz Results</h3>", unsafe_allow_html=True)
            

        # Display Quiz Results
        if not all_results:
            st.info("No quiz results are available yet.")
        else:
            for result in all_results:
                st.write(f"**Student ID**: {result[0]}")
                st.write(f"**Lecture**: {result[1]}")
                st.write(f"**Difficulty**: {result[2]}")
                st.write(f"**Score**: {result[3]}/{result[4]}")
                st.write(f"**Date**: {result[5]}")
                st.write("---")
