import os
import pytest
from conceptual_assignments import save_assignment_to_doc

TEST_GENERATED_DIR = "test_generated_assignments"
os.makedirs(TEST_GENERATED_DIR, exist_ok=True)

@pytest.fixture
def cleanup_generated_dir():
    yield
    for file in os.listdir(TEST_GENERATED_DIR):
        os.remove(os.path.join(TEST_GENERATED_DIR, file))
    os.rmdir(TEST_GENERATED_DIR)

def test_save_assignment_to_doc(cleanup_generated_dir):
    """Test saving generated assignment to a text file."""
    assignment_text = "This is a test assignment."
    title = "Test_Lecture"
    file_path = save_assignment_to_doc(assignment_text, title)

    # Verify the file exists and content matches
    assert os.path.exists(file_path)
    with open(file_path, "r", encoding="utf-8") as f:
        assert f.read() == assignment_text
