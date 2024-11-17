import streamlit as st
from auth import login, register, logout, init_session_state, role_protect
from components.dashboard import dashboard
from components.lecture_summaries import lecture_summaries
from components.conceptual_examples import conceptual_examples
from components.quizzes import quizzes
from components.progress_tracking import progress_tracking
from components.feedback import feedback


# Initialize session state
init_session_state()

# Set page configuration
st.set_page_config(page_title="AI-Powered Teaching Assistant", layout="wide")

# Sidebar Navigation and Authentication
if st.session_state["logged_in"]:
    st.sidebar.markdown(f"### Logged in as: {st.session_state['user']['role'].capitalize()}")
    st.sidebar.button("Logout", on_click=logout)
else:
    # Add Login/Register Navigation in Sidebar
    auth_page = st.sidebar.radio("Authenticate", ["Login", "Register"])
    if auth_page == "Login":
        login()
    elif auth_page == "Register":
        register()
    st.stop()  # Prevent navigation to other pages without login

# Display app pages if logged in
st.title("Smart Teaching Assistant for RE")

# Sidebar navigation
page = st.sidebar.radio("Go to", [
    "Dashboard",
    "Lecture Summaries",
    "Conceptual Examples",
    "Adaptive Quizzes",
    "Progress Tracking",
    "Feedback"
])

# Render the selected page
if page == "Dashboard":
    dashboard()
elif page == "Lecture Summaries":
    role_protect("teacher")  # Protect access to uploading/deleting content
    lecture_summaries()
elif page == "Conceptual Examples":
    conceptual_examples()
elif page == "Adaptive Quizzes":
    quizzes()
elif page == "Progress Tracking":
    progress_tracking()
elif page == "Feedback":
    feedback()
