import openai
import streamlit as st
import PyPDF2
import relevance_check
import os
from dotenv import load_dotenv

# Set up OpenAI API key
if os.getenv("RENDER") is None:  # Render sets RENDER environment variable
    load_dotenv()

# Set OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

# Initialize session state variables if they don’t already exist
if "response_text" not in st.session_state:
    st.session_state.response_text = ""
if "show_chatbox" not in st.session_state:
    st.session_state.show_chatbox = False
if "response_generated" not in st.session_state:
    st.session_state.response_generated = False
if "relevance_shown" not in st.session_state:
    st.session_state.relevance_shown = False

# Close button to hide the chatbox
if st.session_state.show_chatbox:
    if st.button("Close Chatbox"):
        st.session_state.show_chatbox = False
        st.session_state.response_text = ""

# Streamlit app setup
st.title("EduChat")

# Define two columns
col1, col2 = st.columns([1, 1])  # Adjust width ratio as needed

# Left column: PDF upload and input area
with col1:
    st.write("Upload a PDF")
    uploaded_file = st.file_uploader("Upload a PDF file", type="pdf")

    # Extract PDF content
    pdf_content = ""
    if uploaded_file is not None:
        try:
            # Read PDF
            pdf_reader = PyPDF2.PdfReader(uploaded_file)
            pdf_content = "\n".join([page.extract_text() for page in pdf_reader.pages])
            st.success("PDF content extracted successfully.")
        except Exception as e:
            st.error("Failed to read PDF content. Please check the file format.")

    # User input for chatbot prompt
    user_input = st.text_input("Ask a question based on the PDF content:")

# Generate a response only when there’s a user input, PDF content, and no response generated
if user_input and pdf_content and not st.session_state.response_generated:
    full_context = f"PDF content:\n{pdf_content}\n\nUser's question: {user_input}"

    try:
        # Call OpenAI API with the gpt-4o-mini model
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a helpful assistant who can answer questions based on provided PDF content."},
                {"role": "user", "content": full_context}
            ]
        )
        chatbot_response = response['choices'][0]['message']['content']

        # Store the response and set the chatbox to show
        st.session_state.response_text = chatbot_response
        st.session_state.show_chatbox = True
        st.session_state.response_generated = True

    except Exception as e:
        st.error("An error occurred while generating a response. Please try again.")

# Right column: Display a read-only chatbox if `show_chatbox` is True
if st.session_state.show_chatbox:
    with col2:
        st.write("Chatbot Response:")

        # Display the chatbox content
        st.markdown(
            f"""
            <div style="max-height: 300px; overflow-y: auto; padding: 10px; background-color: #f9f9f9; border-radius: 5px;">
                {st.session_state.response_text}
            </div>
            """,
            unsafe_allow_html=True
        )

# Add a button to calculate relevance
if st.button("Calculate Relevance Scores"):
    st.session_state.relevance_shown = True

# Display relevance scores if the button has been clicked
if st.session_state.relevance_shown:
    with st.spinner("Calculating relevance scores..."):
        semantic_similarity = relevance_check.calculate_semantic_similarity(pdf_content, st.session_state.response_text)
        keyword_overlap = relevance_check.calculate_keyword_overlap(pdf_content, st.session_state.response_text)
        feedback_score, feedback_details = relevance_check.calculate_feedback_score(pdf_content, st.session_state.response_text)

    st.write("### Relevance Scores:")
    st.write(f"- **Semantic Similarity:** {semantic_similarity}")
    st.write(f"- **Keyword Overlap:** {keyword_overlap * 100:.2f}%")
    st.write(f"- **LLM Feedback Score:** {feedback_score}")
    st.write(f"- **LLM Feedback Details:** {feedback_details}")

# Reset response state if new input is given
if user_input and not st.session_state.response_generated:
    st.session_state.response_generated = False
    st.session_state.relevance_shown = False
