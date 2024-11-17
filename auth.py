import streamlit as st
from db import authenticate_user, register_user, get_user_role

# Initialize session state for authentication
def init_session_state():
    if "user" not in st.session_state:
        st.session_state["user"] = None  # Stores the logged-in user's details (id and role)
    if "logged_in" not in st.session_state:
        st.session_state["logged_in"] = False  # Tracks whether a user is logged in


# Display the login form
def login():
    st.title("Login")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        user = authenticate_user(email, password)
        if user:
            st.session_state["user"] = user  # Save user details to session state
            st.session_state["logged_in"] = True
            st.success("Login successful!")
            st.rerun()
        else:
            st.error("Invalid email or password")


# Display the registration form (for adding new users)
def register():
    st.title("Register")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    role = st.selectbox("Role", ["teacher", "student"])

    if st.button("Register"):
        if register_user(email, password, role):
            st.success("Registration successful! You can now log in.")
            st.query_params.page = "login"
        else:
            st.error("Email already exists. Please try a different one.")


# Logout the current user
def logout():
    st.session_state["user"] = None
    st.session_state["logged_in"] = False
    st.success("Logged out successfully!")

# Check if the current user has a specific role
def has_role(required_role):
    if st.session_state["user"]:
        user_role = st.session_state["user"]["role"]
        return user_role == required_role
    return False


# Protect a page based on roles
def role_protect(required_role):
    if not st.session_state["logged_in"]:
        st.warning("You must be logged in to access this page.")
        st.stop()
