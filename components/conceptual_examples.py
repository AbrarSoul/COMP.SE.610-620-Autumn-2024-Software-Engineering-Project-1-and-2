import os
import streamlit as st
from db import get_lectures  # Import the function to retrieve lecture PDFs from the database
from pdf_extractor import extract_text_from_pdf  # Custom function to extract text
from relevance_check import calculate_semantic_similarity, calculate_keyword_overlap, calculate_feedback_score
import pandas as pd
import openai  # Library to interact with GPT-4o mini API
import time  # For simulating typing effect

# Set up OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY", "API KEY")


def generate_content(prompt):
    """Generate content based on a user prompt using GPT-4o."""
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are an assistant that generates conceptual examples, summaries, and key contents based on PDF content."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=500
        )
        return response["choices"][0]["message"]["content"]
    except Exception as e:
        return f"Error generating content: {e}"


def typing_effect(text):
    """Simulate a typing effect."""
    placeholder = st.empty()
    typed_text = ""
    for char in text:
        typed_text += char
        placeholder.markdown(typed_text + "▌")
        time.sleep(0.01)
    placeholder.markdown(typed_text)


def conceptual_examples():
    st.markdown("<h1 style='color: #4CAF50;'>Studying Lectures</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='color: #362f2f; font-weight: bold;'>Choose a lecture from the below list and study</h3>", unsafe_allow_html=True)

    # Fetch lectures
    lectures = get_lectures()
    if not lectures:
        st.write("No lecture summaries available.")
        return

    lecture_data = pd.DataFrame(lectures, columns=["ID", "Title", "Upload Date", "File Path"])
    lecture_titles = lecture_data["Title"].tolist()
    selected_lecture_title = st.selectbox("Select a lecture:", lecture_titles)

    # Extract file path
    selected_lecture_path = lecture_data.loc[lecture_data["Title"] == selected_lecture_title, "File Path"].values[0]

    # Extract PDF content
    extracted_text = extract_text_from_pdf(selected_lecture_path)
    if not extracted_text:
        st.warning("Unable to extract content from this PDF. It might be image-based.")
        return

    # Initialize session state variables
    if "generated_content" not in st.session_state:
        st.session_state.generated_content = None
    if "relevance_summary" not in st.session_state:
        st.session_state.relevance_summary = None

    # Buttons for features
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("Generate Conceptual Example"):
            prompt = f"Generate a conceptual example based on the following content:\n\n{extracted_text}"
            st.session_state.generated_content = generate_content(prompt)
            st.session_state.relevance_summary = None
            typing_effect(st.session_state.generated_content)

    with col2:
        if st.button("Generate Summary"):
            prompt = f"Generate a concise summary of the following content:\n\n{extracted_text}"
            st.session_state.generated_content = generate_content(prompt)
            st.session_state.relevance_summary = None
            typing_effect(st.session_state.generated_content)

    with col3:
        if st.button("Find Contents"):
            prompt = f"List the key contents or sections in the following content:\n\n{extracted_text}"
            st.session_state.generated_content = generate_content(prompt)
            st.session_state.relevance_summary = None
            typing_effect(st.session_state.generated_content)

    # Relevance Check Button
    if st.session_state.generated_content:
        st.markdown("### Check the Relevance of Generated Content")
        if st.button("Check Relevance"):
            # Calculate relevance
            semantic_score = calculate_semantic_similarity(extracted_text, st.session_state.generated_content)
            keyword_overlap = calculate_keyword_overlap(extracted_text, st.session_state.generated_content)
            feedback_score, _ = calculate_feedback_score(extracted_text, st.session_state.generated_content)

            # Save to session state to avoid reset
            st.session_state.relevance_summary = {
                "Semantic Similarity": f"{semantic_score:.2f}",
                "Keyword Overlap": f"{keyword_overlap:.2%}",
                "LLM Feedback Score": feedback_score if feedback_score else "N/A"
            }

        # Display relevance summary
        if st.session_state.relevance_summary:
            st.success("Relevance Check Summary:")
            for key, value in st.session_state.relevance_summary.items():
                st.write(f"**{key}**: {value}")

    # Custom prompt feature
    st.markdown("<h3 style='color: #362f2f; font-weight: bold;'>Ask anything if you want to know more about the lecture:</h3>", unsafe_allow_html=True)
    user_prompt = st.text_area("Enter your prompt here (related to the selected lecture):")
    if st.button("Generate Custom Response"):
        if user_prompt.strip():
            full_prompt = f"Based on the following content from the lecture titled '{selected_lecture_title}':\n\n{extracted_text}\n\n{user_prompt}"
            st.session_state.generated_content = generate_content(full_prompt)
            st.session_state.relevance_summary = None
            typing_effect(st.session_state.generated_content)
        else:
            st.warning("Please enter a custom prompt to generate a response.")

    # Relevance Check for Custom Response
    if st.session_state.generated_content and st.button("Check Custom Response Relevance"):
        semantic_score = calculate_semantic_similarity(extracted_text, st.session_state.generated_content)
        keyword_overlap = calculate_keyword_overlap(extracted_text, st.session_state.generated_content)
        feedback_score, _ = calculate_feedback_score(extracted_text, st.session_state.generated_content)

        # Save to session state
        st.session_state.relevance_summary = {
            "Semantic Similarity": f"{semantic_score:.2f}",
            "Keyword Overlap": f"{keyword_overlap:.2%}",
            "LLM Feedback Score": feedback_score if feedback_score else "N/A"
        }

    if st.session_state.relevance_summary:
        st.success("Relevance Check Summary:")
        for key, value in st.session_state.relevance_summary.items():
            st.write(f"**{key}**: {value}")


if __name__ == "__main__":
    conceptual_examples()
