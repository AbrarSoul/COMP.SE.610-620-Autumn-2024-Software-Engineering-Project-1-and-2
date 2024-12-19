from unittest.mock import patch
from conceptual_assignments import generate_conceptual_assignment, save_assignment_to_doc

def test_generate_conceptual_assignment():
    """Test generating conceptual assignment successfully."""
    with patch("openai.ChatCompletion.create") as mock_gpt:
        mock_gpt.return_value = {"choices": [{"message": {"content": "Test assignment content."}}]}
        response = generate_conceptual_assignment("Test Lecture")
        assert response == "Test assignment content."

def test_generate_conceptual_assignment_failure():
    """Test handling failure in generating conceptual assignments."""
    with patch("openai.ChatCompletion.create", side_effect=Exception("API Error")):
        response = generate_conceptual_assignment("Test Lecture")
        assert response is None

def test_save_assignment_to_doc():
    """Test saving generated assignment to a document."""
    content = "Test generated assignment."
    file_path = save_assignment_to_doc(content, "Test_Lecture")
    assert file_path.endswith("Test_Lecture_assignment.txt")
