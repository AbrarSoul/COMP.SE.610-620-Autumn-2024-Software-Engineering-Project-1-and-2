import streamlit as st
import pandas as pd
from db import init_db, save_to_db, get_lectures, delete_from_db  # Extend database functions
from datetime import datetime
import os

# Ensure that the upload directory exists
UPLOAD_DIR = 'uploaded_pdfs'
os.makedirs(UPLOAD_DIR, exist_ok=True)

def lecture_summaries():
    # Initialize the database (create tables if they don't exist)
    init_db()

    # Lecture Summaries Header
    st.markdown('<div class="lecture-header">Lecture Materials</div>', unsafe_allow_html=True)
    
    # Upload section
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
    st.markdown('<div class="subheader">Uploaded Lecture Summaries</div>', unsafe_allow_html=True)
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
                if st.button("Delete", key=f"delete_{row['ID']}"):
                    delete_file(row["ID"], row["File Path"])
    else:
        st.write("No lectures uploaded yet.")

#Delete uploaded lectures
def delete_file(lecture_id, file_path):
    """Delete a file and its database entry."""
    if os.path.exists(file_path):
        os.remove(file_path)
    delete_from_db(lecture_id)
    st.success("Lecture deleted successfully!")


