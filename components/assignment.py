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
                    # Display the generated assignment in the UI
                    st.markdown("### Generated Assignment:")
                    st.markdown(f"**Assignment Description:**\n\n{generated_assignment}", unsafe_allow_html=False)

                    # Save the assignment to a PDF file
                    pdf_filename = f"{selected_lecture_title}_assignment.pdf"
                    pdf_file_path = os.path.join(GENERATED_DIR, pdf_filename)
                    
                    try:
                        from reportlab.lib.pagesizes import letter
                        from reportlab.pdfgen import canvas

                        # Save the generated content as a PDF
                        c = canvas.Canvas(pdf_file_path, pagesize=letter)
                        c.setFont("Helvetica", 12)
                        y_position = 750  # Start position for the text
                        line_height = 15

                        for line in generated_assignment.split("\n"):
                            if y_position < 50:  # Create a new page if out of space
                                c.showPage()
                                c.setFont("Helvetica", 12)
                                y_position = 750
                            c.drawString(50, y_position, line)
                            y_position -= line_height
                        
                        c.save()
                    except Exception as e:
                        st.error(f"Error saving PDF: {e}")

                    # Display download button for the generated PDF
                    with open(pdf_file_path, "rb") as pdf_file:
                        st.download_button(
                            label="Download Generated Assignment (PDF)",
                            data=pdf_file,
                            file_name=pdf_filename,
                            mime="application/pdf"
                        )

                    # Save the generated assignment in the database
                    save_generated_assignment(selected_lecture_title, generated_assignment)

        # View Submitted Assignments
        st.subheader("Your Submitted Assignments")
        student_assignments = get_student_assignments(user["id"])
        if not student_assignments:
            st.info("No submissions found.")
        else:
            for assignment in student_assignments:
                st.write(f"**Assignment Title**: {assignment[0]}")
                if assignment[2]:  # Check if the submission file path exists
                    st.download_button(
                        label="Download Your Submission",
                        data=open(assignment[2], "rb"),
                        file_name=os.path.basename(assignment[2]),
                        mime="application/pdf"
                    )
                else:
                    st.warning("No file submitted for this assignment.")
                st.write("---")

        # Submit Assignment
        st.markdown("### Submit Your Completed Assignment")
        with st.form("submission_form"):
            student_email = st.text_input("Your Email Address", "")
            uploaded_file = st.file_uploader("Upload Assignment (PDF only)", type=["pdf"])
            submitted = st.form_submit_button("Submit Assignment")
            if submitted:
                if not student_email:
                    st.error("Please provide your email address before submitting.")
                elif not uploaded_file:
                    st.error("Please upload your assignment as a PDF.")
                else:
                    file_path = save_uploaded_pdf(uploaded_file, student_email)
                    submit_student_assignment(user["id"], student_email, selected_lecture_title, file_path)
                    st.success("Assignment submitted successfully!")

    # Teacher View: Display Submitted Assignments
    elif user["role"] == "teacher":
        st.subheader("Teacher Dashboard: View All Assignments")

        # Filter Section
        st.markdown("### Filter by Student ID or Email")
        col1, col2 = st.columns(2)
        with col1:
            student_id_filter = st.text_input("Enter Student ID (optional):")
        with col2:
            email_filter = st.text_input("Enter Email ID (optional):")

        # Fetch all assignments
        assignments = get_all_assignments()

        # Apply filters
        if student_id_filter or email_filter:
            if student_id_filter:
                assignments = [a for a in assignments if str(a[0]) == student_id_filter]
            if email_filter:
                assignments = [a for a in assignments if a[1] and email_filter.lower() in a[1].lower()]

            st.markdown(f"### Showing Filtered Results for Student ID: `{student_id_filter}` or Email: `{email_filter}`")
        else:
            st.markdown("### Showing All Assignments")

        # Display Assignments
        if not assignments:
            st.info("No assignments found.")
        else:
            for idx, assignment in enumerate(assignments):
                st.write(f"### **Assignment Block**")
                st.write(f"**Student ID**: {assignment[0]}")
                st.write(f"**Email ID**: {assignment[1]}")
                st.write(f"**Assignment Title**: {assignment[2]}")

                # Display Generated Assignment
                if assignment[3]:
                    doc_file_path = save_assignment_to_doc(assignment[3], assignment[2])
                    st.write("**Generated Assignment:**")
                    st.download_button(
                        label="Download Generated Assignment",
                        data=open(doc_file_path, "rb"),
                        file_name=os.path.basename(doc_file_path),
                        key=f"assignment_generated_{idx}"
                    )

                # Display Submitted Assignment
                if assignment[4]:
                    st.write("**Submitted Assignment:**")
                    st.download_button(
                        label="Download Submitted Assignment",
                        data=open(assignment[4], "rb"),
                        file_name=os.path.basename(assignment[4]),
                        key=f"assignment_submitted_{idx}"
                    )
                else:
                    st.warning("No assignment submitted for this lecture.")
                st.write("---")

if __name__ == "__main__":
    conceptual_assignments()
