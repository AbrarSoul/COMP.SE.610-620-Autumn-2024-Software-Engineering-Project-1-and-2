import streamlit as st
from auth import init_session_state, logout

def test_session_state_initialization():
    """Test that session state initializes correctly."""
    if "user" in st.session_state:
        del st.session_state["user"]  # Ensure session starts fresh
    init_session_state()
    assert "user" in st.session_state
    assert st.session_state["user"] is None
    assert "logged_in" in st.session_state
    assert st.session_state["logged_in"] is False

def test_logout_functionality():
    """Test that logout clears session state."""
    st.session_state["user"] = {"id": 1, "role": "teacher"}
    st.session_state["logged_in"] = True
    logout()
    assert st.session_state["user"] is None
    assert st.session_state["logged_in"] is False
