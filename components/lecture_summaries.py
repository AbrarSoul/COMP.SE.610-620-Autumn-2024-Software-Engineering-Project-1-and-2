import streamlit as st
import pandas as pd
from db import init_db, save_to_db, get_lectures, delete_from_db
from auth import has_role
from datetime import datetime
import os

# Ensure that the upload directory exists
UPLOAD_DIR = 'uploaded_pdfs'
os.makedirs(UPLOAD_DIR, exist_ok=True)


def lecture_summaries():
    # Initialize the database (create tables if they don't exist)
    init_db()

    # Lecture Summaries Header
    st.markdown("<h1 style='color: #4CAF50;'>Lecture Materials</h1>", unsafe_allow_html=True)

    # Role-based display for upload section
    if has_role("teacher"):
        st.markdown('<div class="subheader">Upload Lectures</div>', unsafe_allow_html=True)
        uploaded_file = st.file_uploader("Upload Lecture PDF", type="pdf")
        if uploaded_file is not None:
            # Save file to the local directory
            file_path = os.path.join(UPLOAD_DIR, uploaded_file.name.replace(" ", "_"))
            with open(file_path, "wb") as f:
                f.write(uploaded_file.getbuffer())

            # Save lecture information to the database
            save_to_db(uploaded_file.name, file_path)

            # Display success message
            st.markdown('<div class="upload-success">Uploaded successfully!</div>', unsafe_allow_html=True)

    # Display uploaded lectures from the database
    st.markdown("<h3 style='color: #362f2f; font-weight: bold;'>Uploaded Lecture Summaries</h3>", unsafe_allow_html=True)
    lectures = get_lectures()
    if lectures:
        # Convert data to DataFrame for easy display
        lecture_data = pd.DataFrame(lectures, columns=["ID", "Title", "Upload Date", "File Path"])
        for _, row in lecture_data.iterrows():
            col1, col2 = st.columns([4, 2])
            with col1:
                st.markdown(f"""
                    <div class="lecture-row">
                        <strong>{row["Title"]}</strong> <br>
                        <small>Uploaded on: {row["Upload Date"]}</small>
                    </div>
                """, unsafe_allow_html=True)
            with col2:
                # Disable delete button for students
                if has_role("teacher"):
                    if st.button("Delete", key=f"delete_{row['ID']}"):
                        delete_file(row["ID"], row["File Path"])
                else:
                    st.button("Delete", key=f"disabled_delete_{row['ID']}", disabled=True)
    else:
        st.write("No lectures uploaded yet.")


# Delete uploaded lectures
def delete_file(lecture_id, file_path):
    """Delete a file and its database entry."""
    if os.path.exists(file_path):
        os.remove(file_path)
    delete_from_db(lecture_id)
    st.success("Lecture deleted successfully!")
