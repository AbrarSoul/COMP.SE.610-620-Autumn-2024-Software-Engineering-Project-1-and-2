import pytest
import streamlit as st
from unittest.mock import MagicMock, patch
from auth import init_session_state, login, register, logout, has_role

@pytest.fixture
def mock_session_state(mocker):
    """Fixture to mock Streamlit session state."""
    mocker.patch.object(st, "session_state", {})
    init_session_state()


def test_init_session_state(mock_session_state):
    """Test session state initialization."""
    assert "user" in st.session_state
    assert st.session_state["user"] is None
    assert "logged_in" in st.session_state
    assert st.session_state["logged_in"] is False


# def test_login_success(mocker, mock_session_state):
#     """Test successful login."""
#     mocker.patch("db.authenticate_user", return_value={"id": 1, "role": "teacher"})
#     st.text_input = MagicMock(side_effect=["test@example.com", "password123"])
#     st.button = MagicMock(return_value=True)
#
#     # Simulate login function
#     login()
#     assert st.session_state["logged_in"] is True
#     assert st.session_state["user"]["role"] == "teacher"


def test_login_failure(mocker, mock_session_state):
    """Test failed login."""
    mocker.patch("db.authenticate_user", return_value=None)
    st.text_input = MagicMock(side_effect=["test@example.com", "wrongpassword"])
    st.button = MagicMock(return_value=True)

    # Simulate login function
    login()
    assert st.session_state["logged_in"] is False
    assert st.session_state["user"] is None


def test_register_success(mocker, mock_session_state):
    """Test successful registration."""
    mocker.patch("db.register_user", return_value=True)
    st.text_input = MagicMock(side_effect=["test@example.com", "password123"])
    st.selectbox = MagicMock(return_value="teacher")
    st.button = MagicMock(return_value=True)

    # Simulate register function
    register()


def test_logout(mock_session_state):
    """Test logout functionality."""
    st.session_state["logged_in"] = True
    st.session_state["user"] = {"id": 1, "role": "teacher"}

    # Simulate logout function
    logout()
    assert st.session_state["logged_in"] is False
    assert st.session_state["user"] is None


def test_has_role(mock_session_state):
    """Test role checking."""
    st.session_state["user"] = {"id": 1, "role": "teacher"}
    assert has_role("teacher") is True
    assert has_role("student") is False
