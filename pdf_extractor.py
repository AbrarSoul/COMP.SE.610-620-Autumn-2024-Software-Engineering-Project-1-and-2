import fitz  # PyMuPDF

def extract_text_from_pdf(pdf_path):
    """Extracts text from a PDF file."""
    text = ""
    try:
        with fitz.open(pdf_path) as pdf:
            for page_num in range(pdf.page_count):
                page = pdf[page_num]
                text += page.get_text("text")  # Extract text from each page
    except Exception as e:
        text = f"Error extracting text: {str(e)}"
    return text
