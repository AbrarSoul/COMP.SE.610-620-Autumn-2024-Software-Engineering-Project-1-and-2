import streamlit as st
import PyPDF2
import openai

# Set your OpenAI API key
openai.api_key = "open_api_key"

def extract_text_from_pdf(pdf_file):
    """Extract text from a PDF file."""
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text

def generate_quiz_gpt4_mini(text, num_questions=5):
    """Generate mcq quiz questions using the gpt-4o-mini model."""
    prompt = (
        f"Based on the following content, create {num_questions} quiz questions:\n\n"
        f"{text[:3000]}..."  # Limit input to the first 3000 characters to fit model constraints
        f"\n\nProvide the questions clearly numbered."
    )
    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=500,
        temperature=0.7
    )
    return response["choices"][0]["message"]["content"].strip()

def main():
    st.title("Quiz")
    st.write("Generate quiz to assess yourself")

    uploaded_file = st.file_uploader("Upload a PDF", type="pdf")

    if uploaded_file is not None:
        st.write("Extracting text from the PDF...")
        pdf_text = extract_text_from_pdf(uploaded_file)

        st.write("PDF Text Extracted. Ready to generate a quiz!")
        num_questions = st.slider("Select the number of questions:", 1, 10, 5)
        
        if st.button("Generate Quiz"):
            with st.spinner("Generating quiz..."):
                try:
                    quiz = generate_quiz_gpt4_mini(pdf_text, num_questions)
                    st.success("Quiz Generated!")
                    st.text_area("Generated Quiz", value=quiz, height=300)
                except Exception as e:
                    st.error(f"Error generating quiz: {e}")

if __name__ == "__main__":
    main()
