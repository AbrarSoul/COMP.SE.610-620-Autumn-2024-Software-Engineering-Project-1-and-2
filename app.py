import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

# Set page configuration
st.set_page_config(page_title="AI-Powered Teaching Assistant", layout="wide")
st.title("Smart Teaching Assistant for RE")

# Import components
from components.dashboard import dashboard
from components.lecture_summaries import lecture_summaries
from components.conceptual_examples import conceptual_examples
from components.quizzes import quizzes
from components.progress_tracking import progress_tracking
from components.feedback import feedback

# Function to load and apply external CSS
def load_css(file_name):
    with open(file_name, encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Load CSS file
load_css("style.css")

# Sidebar navigation and page routing
page = st.sidebar.radio("Go to", ["Dashboard", "Lecture Summaries", "Conceptual Examples", "Adaptive Quizzes", "Progress Tracking", "Feedback"])

if page == "Dashboard":
    dashboard()
elif page == "Lecture Summaries":
    lecture_summaries()
elif page == "Conceptual Examples":
    conceptual_examples()
elif page == "Adaptive Quizzes":
    quizzes()
elif page == "Progress Tracking":
    progress_tracking()
elif page == "Feedback":
    feedback()
