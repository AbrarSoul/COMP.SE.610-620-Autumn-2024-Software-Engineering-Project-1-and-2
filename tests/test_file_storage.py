import os
import pytest
from file_storage import save_uploaded_pdf

TEST_UPLOAD_DIR = "test_uploads"
os.makedirs(TEST_UPLOAD_DIR, exist_ok=True)

@pytest.fixture
def cleanup_upload_dir():
    yield
    for file in os.listdir(TEST_UPLOAD_DIR):
        os.remove(os.path.join(TEST_UPLOAD_DIR, file))
    os.rmdir(TEST_UPLOAD_DIR)

def test_save_uploaded_pdf(tmp_path, cleanup_upload_dir):
    """Test saving an uploaded PDF file."""
    test_file_content = b"Test PDF Content"
    test_file_name = "test_assignment.pdf"
    test_student_name = "John_Doe"

    # Simulate an uploaded file
    uploaded_file = tmp_path / test_file_name
    uploaded_file.write_bytes(test_file_content)

    # Save the file
    file_path = save_uploaded_pdf(open(uploaded_file, "rb"), test_student_name)

    # Verify file was saved correctly
    assert os.path.exists(file_path)
    with open(file_path, "rb") as f:
        assert f.read() == test_file_content
