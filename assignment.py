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

def generate_assignment_gpt4_mini(text):
    """Generate a real-life scenario-based assignment using GPT-4o-mini."""
    prompt = (
        f"Create a real-life scenario-based assignment based on the following text. The assignment should include:\n"
        f"1. A detailed description of the scenario.\n"
        f"2. Specific tasks/questions for the students to address based on the scenario.\n"
        f"3. Expected outcomes or learning objectives for the assignment.\n\n"
        f"Text for reference:\n{text[:3000]}..."  # Limit input to the first 3000 characters
    )
    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=700,
        temperature=0.7
    )
    return response["choices"][0]["message"]["content"].strip()

def main():
    st.title("Assignment")
    st.write("Generate a real-life scenario-based assignment to assess what you have learnt!")

    uploaded_file = st.file_uploader("Upload a PDF", type="pdf")

    if uploaded_file is not None:
        st.write("Extracting text from the PDF...")
        pdf_text = extract_text_from_pdf(uploaded_file)

        st.write("PDF Text Extracted. Ready to generate an assignment!")
        if st.button("Generate Assignment"):
            with st.spinner("Generating assignment..."):
                try:
                    assignment = generate_assignment_gpt4_mini(pdf_text)
                    st.success("Assignment Generated!")
                    st.text_area("Generated Assignment", value=assignment, height=400)
                except Exception as e:
                    st.error(f"Error generating assignment: {e}")

if __name__ == "__main__":
    main()
