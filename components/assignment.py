import os
import streamlit as st
import pandas as pd
from datetime import datetime
import openai  # Library to interact with OpenAI GPT models
from db import (get_lectures, save_generated_assignment, submit_student_assignment, 
                get_all_assignments, get_student_assignments)
from pdf_extractor import extract_text_from_pdf  # For extracting text
from reportlab.pdfgen import canvas  # For generating PDFs
import time  # For typing effect

# Set the OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY", "API KEY")

# Directory for storing submitted and generated assignments
SUBMISSION_DIR = "submitted_assignments"
GENERATED_DIR = "generated_assignments"
os.makedirs(SUBMISSION_DIR, exist_ok=True)
os.makedirs(GENERATED_DIR, exist_ok=True)


def generate_conceptual_assignment(pdf_title):
    """Generate a real-life scenario-based conceptual assignment using GPT-4o."""
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": (
                    "You are an assistant that generates real-world, scenario-based conceptual assignments "
                    "for students. Each assignment must be clear, practical, and tied to real-life situations. "
                    "Ensure it aligns with the given lecture title."
                )},
                {"role": "user", "content": f"Create a real-life scenario-based conceptual assignment based on the lecture titled: '{pdf_title}'"}
            ],
            max_tokens=600
        )
        return response["choices"][0]["message"]["content"]
    except Exception as e:
        st.error(f"Error: {e}")
        return None


def save_assignment_to_doc(assignment_text, title):
    """Save the generated assignment to a text file."""
    try:
        file_path = os.path.join(GENERATED_DIR, f"{title}_assignment.txt")
        # Only save if the file does not already exist
        if not os.path.exists(file_path):
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(assignment_text)
        return file_path
    except Exception as e:
        st.error(f"Error saving generated assignment: {e}")
        return None


def save_uploaded_pdf(uploaded_file, student_name):
    """Save the uploaded assignment PDF to the submissions directory."""
    try:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        file_path = os.path.join(SUBMISSION_DIR, f"{student_name}_{timestamp}.pdf")
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        return file_path
    except Exception as e:
        st.error(f"Error saving the uploaded file: {e}")
        return None


def conceptual_assignments():
    st.markdown("<h1 style='color: #4CAF50;'>Real-Life Scenario-Based Conceptual Assignments</h1>", unsafe_allow_html=True)

    # Fetch user role from session
    user = st.session_state.get("user", {"role": "student", "id": "unknown"})

    # Fetch lectures
    st.info("Fetching available lectures...")
    lectures = get_lectures()
    if not lectures:
        st.warning("No lecture summaries are available for generating assignments. Please upload lecture files.")
        return

    # Convert to DataFrame
    lecture_data = pd.DataFrame(lectures, columns=["ID", "Title", "Upload Date", "File Path"])
    lecture_titles = lecture_data["Title"].tolist()
    selected_lecture_title = st.selectbox("Select a lecture to generate/view assignments:", lecture_titles)

    # Student View: Generate and Submit Assignments
    if user["role"] == "student":
        # Generate Assignment
        if st.button("Generate Conceptual Assignment"):
            with st.spinner("Generating real-life scenario-based assignment..."):
                generated_assignment = generate_conceptual_assignment(selected_lecture_title)
                if generated_assignment:
                    file_path = save_assignment_to_doc(generated_assignment, selected_lecture_title)
                    st.markdown("### Generated Assignment:")
                    st.text_area("Generated Assignment", generated_assignment, height=200, disabled=True)
                    st.success("Assignment generated successfully!")
                    st.download_button(
                        label="Download Assignment as Doc",
                        data=open(file_path, "rb"),
                        file_name=os.path.basename(file_path),
                        mime="text/plain"
                    )
                else:
                    st.error("Failed to generate the assignment. Please try again.")

        # Submit Assignment
        st.markdown("### Submit Your Completed Assignment")
        with st.form("submission_form"):
            student_name = st.text_input("Your Name", "")
            uploaded_file = st.file_uploader("Upload Assignment (PDF only)", type=["pdf"])
            submitted = st.form_submit_button("Submit Assignment")
            if submitted:
                if not student_name:
                    st.error("Please provide your name before submitting.")
                elif not uploaded_file:
                    st.error("Please upload your assignment as a PDF.")
                else:
                    file_path = save_uploaded_pdf(uploaded_file, student_name)
                    submit_student_assignment(user["id"], student_name, selected_lecture_title, file_path)
                    st.success("Assignment submitted successfully!")

    # Teacher View: Display Submitted Assignments
    elif user["role"] == "teacher":
        st.subheader("All Submitted Assignments")
        assignments = get_all_assignments()
        if not assignments:
            st.info("No assignments submitted yet.")
        else:
            for assignment in assignments:
                st.write(f"**Student Name**: {assignment[1]}")
                st.write(f"**Assignment Title**: {assignment[2]}")

                # Link to download LLM-generated assignment
                if assignment[3]:
                    doc_file_path = save_assignment_to_doc(assignment[3], assignment[2])
                    st.download_button("Download Generated Assignment", open(doc_file_path, "rb"), file_name=os.path.basename(doc_file_path))

                # Link to student submission (PDF)
                if assignment[4]:
                    st.download_button("Download Submitted PDF", open(assignment[4], "rb"), file_name=os.path.basename(assignment[4]))
                st.write("---")

    # Student View: View Own Submissions
    else:
        st.subheader("Your Submitted Assignments")
        student_assignments = get_student_assignments(user["id"])
        if not student_assignments:
            st.info("No submissions found.")
        else:
            for assignment in student_assignments:
                st.write(f"**Assignment Title**: {assignment[0]}")
                st.download_button("Download Your Submission", open(assignment[2], "rb"), file_name=os.path.basename(assignment[2]))
                st.write("---")


if __name__ == "__main__":
    conceptual_assignments()
