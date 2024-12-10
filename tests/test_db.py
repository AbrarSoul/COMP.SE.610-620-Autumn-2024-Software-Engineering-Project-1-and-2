import sqlite3
import os
import pytest
from db import init_db, save_to_db, get_lectures, delete_from_db, register_user, authenticate_user, submit_feedback, get_all_feedback

# Path for a temporary test database
TEST_DB_PATH = "test_lecture_summaries.db"

@pytest.fixture
def setup_database(mocker):
    """Fixture to set up and tear down the test database."""
    # Mock DB_PATH to use a test database
    mocker.patch("db.DB_PATH", TEST_DB_PATH)
    init_db()  # Initialize the test database
    yield
    os.remove(TEST_DB_PATH)  # Clean up after tests


def test_init_db(setup_database):
    """Test database initialization."""
    conn = sqlite3.connect(TEST_DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = [row[0] for row in cursor.fetchall()]
    conn.close()
    assert "lectures" in tables
    assert "users" in tables


def test_save_to_db(setup_database):
    """Test saving a lecture to the database."""
    save_to_db("Test Lecture", "test_path.pdf")
    lectures = get_lectures()
    assert len(lectures) == 1
    assert lectures[0][1] == "Test Lecture"
    assert lectures[0][3] == "test_path.pdf"


def test_delete_from_db(setup_database):
    """Test deleting a lecture from the database."""
    save_to_db("Test Lecture", "test_path.pdf")
    lectures = get_lectures()
    delete_from_db(lectures[0][0])
    lectures_after_delete = get_lectures()
    assert len(lectures_after_delete) == 0


def test_register_user(setup_database):
    """Test registering a new user."""
    success = register_user("test@example.com", "password123", "teacher")
    assert success is True

    # Attempt to register the same user again
    duplicate = register_user("test@example.com", "password123", "teacher")
    assert duplicate is False


def test_authenticate_user(setup_database):
    """Test user authentication."""
    register_user("test@example.com", "password123", "teacher")
    user = authenticate_user("test@example.com", "password123")
    assert user is not None
    assert user["role"] == "teacher"

    # Test authentication with incorrect credentials
    invalid_user = authenticate_user("test@example.com", "wrongpassword")
    assert invalid_user is None

def test_feedback_submission(setup_database):
    """Test submitting anonymous feedback."""
    feedback_text = "This is a test feedback."
    submit_feedback(feedback_text)
    feedback_data = get_all_feedback()
    assert len(feedback_data) == 1
    assert feedback_data[0][0] == feedback_text


def test_get_all_feedback_empty(setup_database):
    """Test retrieving feedback when the table is empty."""
    feedback_data = get_all_feedback()
    assert len(feedback_data) == 0
