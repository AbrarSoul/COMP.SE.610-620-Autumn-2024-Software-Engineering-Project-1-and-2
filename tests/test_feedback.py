import pytest
from db import submit_feedback, get_all_feedback

@pytest.fixture
def setup_feedback_table(mocker):
    """Setup the feedback table for testing."""
    mocker.patch("db.init_feedback_table")
    submit_feedback("This is test feedback.")

def test_submit_feedback(setup_feedback_table):
    """Test submitting feedback."""
    feedback = get_all_feedback()
    assert len(feedback) == 1
    assert feedback[0][0] == "This is test feedback."

def test_empty_feedback_table(mocker):
    """Test retrieving feedback when no feedback exists."""
    mocker.patch("db.get_all_feedback", return_value=[])
    feedback = get_all_feedback()
    assert len(feedback) == 0
