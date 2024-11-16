import os

UPLOAD_DIR = 'uploaded_pdfs'
os.makedirs(UPLOAD_DIR, exist_ok=True)

def save_file(file, filename):
    filename = filename.replace(" ", "_")  # Replace spaces with underscores
    file_path = os.path.join(UPLOAD_DIR, filename)
    with open(file_path, "wb") as f:
        f.write(file.getbuffer())
    return file_path
