import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

def dashboard():
    st.markdown('<div class="dashboard-header">Dashboard Overview</div>', unsafe_allow_html=True)

    # Overall Course Progress with dynamic color based on progress
    st.markdown('<div class="subheader">Overall Course Progress</div>', unsafe_allow_html=True)
    overall_progress = 0.55  # Example progress percentage (55%)
    progress_color = "#4CAF50" if overall_progress > 0.7 else "#FFC107" if overall_progress > 0.4 else "#F44336"
    st.markdown(f"""
        <div class="progress-bar">
            <div class="progress-fill" style="width: {overall_progress * 100}%; background-color: {progress_color};"></div>
        </div>
    """, unsafe_allow_html=True)

    # Quick Stats
    st.markdown('<div class="subheader">Quick Stats</div>', unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Assignments", "4", "+1 since last week")
    col2.metric("Upcoming Deadlines", "2", "-1 since last check")
    col3.metric("Feedback Received", "85%", "+5% since last week")

    # Assignment Deadlines with Expander and Filter
    with st.expander("Upcoming Assignment Deadlines", expanded=True):
        assignment_data = {
            "Assignment": ["Lecture Summary Review", "Case Study Analysis", "Requirements Elicitation Report", "Project Planning Document"],
            "Due Date": [
                (datetime.now() + timedelta(days=5)).strftime("%Y-%m-%d"),
                (datetime.now() + timedelta(days=10)).strftime("%Y-%m-%d"),
                (datetime.now() + timedelta(days=15)).strftime("%Y-%m-%d"),
                (datetime.now() + timedelta(days=20)).strftime("%Y-%m-%d")
            ]
        }
        assignment_df = pd.DataFrame(assignment_data)
        st.table(assignment_df)

    # Important Notices
    st.markdown('<div class="subheader">Important Notices</div>', unsafe_allow_html=True)
    with st.expander("Show Notices"):
        st.markdown("""
            <div class="important-notices">
                <p class="notice-item">1. <strong>New Lecture Materials Available</strong>: Check the 'Lecture Summaries' section for recent updates.</p>
                <p class="notice-item">2. <strong>Quiz Deadline</strong>: Complete your adaptive quizzes by the end of the week.</p>
                <p class="notice-item">3. <strong>Feedback Reminder</strong>: Submit feedback on your recent learning materials to help improve the assistant.</p>
            </div>
        """, unsafe_allow_html=True)

    # Enhanced Feedback Section
    st.markdown('<div class="subheader">Feedback Section</div>', unsafe_allow_html=True)
    feedback_text = st.text_area("Your Feedback", "Enter your feedback here...", height=100)
    if st.button("Submit Feedback"):
        st.success("Thank you for your feedback!")
