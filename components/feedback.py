import streamlit as st
from db import init_feedback_table, submit_feedback, get_all_feedback
from auth import has_role

# Ensure the feedback table is initialized
init_feedback_table()


def feedback():
    st.markdown("<h1 style='color: #4CAF50;'>Feedback</h1>", unsafe_allow_html=True)

    # Role-based feedback functionality
    if has_role("student"):
        st.write("We value your feedback to enhance this learning assistant.")
        st.markdown("<h3 style='color: #362f2f; font-weight: bold;'>Submit Feedback (Anonymous)</h3>", unsafe_allow_html=True)
        feedback_text = st.text_area("Your Feedback", placeholder="Enter your feedback here...")
        if st.button("Submit Feedback"):
            if feedback_text.strip():
                submit_feedback(feedback_text)
                st.success("Thank you for your feedback! It has been submitted anonymously.")
            else:
                st.warning("Feedback cannot be empty.")

    elif has_role("teacher"):
        st.markdown("<h3 style='color: #362f2f; font-weight: bold;'>View Feedback</h3>", unsafe_allow_html=True)
        feedback_data = get_all_feedback()

        if feedback_data:
            for feedback_text, submitted_at in feedback_data:
                st.markdown(f"""
                **Submitted At:** {submitted_at}  
                **Feedback:** {feedback_text}
                """)
                st.markdown("---")
        else:
            st.info("No feedback submitted yet.")

    else:
        st.warning("You do not have permission to view or submit feedback.")
