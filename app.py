from flask import Flask, render_template, request
from PyPDF2 import PdfReader
import requests

app = Flask(__name__)

# Hugging Face GPT-Neo API settings
HF_API_URL = "https://api-inference.huggingface.co/models/EleutherAI/gpt-neo-2.7B"
HF_API_KEY = "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" 

headers = {
    "Authorization": f"Bearer {HF_API_KEY}",
    "Content-Type": "application/json"
}

# Function to summarize the text using GPT-Neo
def summarize_text(text):
    # Parameters for generating a concise summary
    data = {
        "inputs": text,
        "parameters": {
            "max_length": 150,   # Limit summary to 150 tokens
            "min_length": 50,    # Minimum length of summary
            "do_sample": True,   # Enable sampling for creative results
            "temperature": 0.7,  # Control randomness (0.7 for balanced creativity)
            "top_p": 0.9,        # Nucleus sampling to focus on high-probability words
            "num_return_sequences": 1  # Generate one summary
        }
    }

    # Debugging: print the text and request details
    print("Sending text to Hugging Face API for summarization...")
    #print(f"Text to summarize (first 500 chars): {text[:500]}")
    
    # Sending the request
    response = requests.post(HF_API_URL, headers=headers, json=data)
    
    # Debugging: print the response status and content
    print(f"API Response Status Code: {response.status_code}")

    response = requests.post(HF_API_URL, headers=headers, json=data)

    if response.status_code == 200:
        try:
            summary = response.json()[0]["generated_text"]
            return summary
        except (IndexError, KeyError):
            return "Error: Could not parse summary from response."
    else:
        return f"Error: {response.status_code}, {response.text}"

# Function to extract text from a PDF
def extract_text_from_pdf(file):
    pdf_reader = PdfReader(file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text

# Function to split large text into chunks
def split_text(text, chunk_size=1000):
    return [text[i:i + chunk_size] for i in range(0, len(text), chunk_size)]

# Function to summarize large texts by splitting them into chunks
def summarize_large_text(text):
    chunks = split_text(text)
    summaries = [summarize_text(chunk) for chunk in chunks]
    return " ".join(summaries)

# Home route to display the upload page
@app.route("/")
def home():
    return render_template("index.html")

# Route to handle PDF uploads and generate summaries
@app.route("/summarize", methods=["POST"])
def summarize_pdf():
    if 'pdf' not in request.files:
        return "No PDF uploaded", 400
    
    file = request.files['pdf']
    text = extract_text_from_pdf(file)
    
    # If the text is too long, split it and summarize each part
    summary = summarize_large_text(text) if len(text) > 1000 else summarize_text(text)
    
    return summary

if __name__ == "__main__":
    app.run(debug=True)