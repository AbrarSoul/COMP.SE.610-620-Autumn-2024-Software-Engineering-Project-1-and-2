import streamlit as st
from db import get_lectures  # Import the function to retrieve lecture PDFs from the database
from pdf_extractor import extract_text_from_pdf  # Import the PDF extraction function
import pandas as pd

def conceptual_examples():
    # Header for the Conceptual Examples section
    st.markdown('<div class="lecture-header">Conceptual Examples</div>', unsafe_allow_html=True)

    # Fetch the list of uploaded lecture PDFs from the database
    lectures = get_lectures()
    if not lectures:
        st.write("No lecture summaries available for extraction.")
        return

    # Convert the lecture data to a DataFrame for easy selection
    lecture_data = pd.DataFrame(lectures, columns=["ID", "Title", "Upload Date", "File Path"])

    # Dropdown for selecting a lecture PDF to extract
    lecture_titles = lecture_data["Title"].tolist()
    selected_lecture_title = st.selectbox("Select a lecture to extract text from:", lecture_titles)

    # Get the file path for the selected lecture
    selected_lecture_path = lecture_data.loc[lecture_data["Title"] == selected_lecture_title, "File Path"].values[0]

    # Display button to extract text from the selected PDF
    if st.button("Extract Text"):
        extracted_text = extract_text_from_pdf(selected_lecture_path)
        
        # Check if any text was extracted, and display it
        if extracted_text:
            st.markdown(f"### Extracted Text from {selected_lecture_title}")
            st.write(extracted_text)  # Display extracted text
        else:
            st.write("No text was extracted from the PDF. It might be an image-based PDF.")
