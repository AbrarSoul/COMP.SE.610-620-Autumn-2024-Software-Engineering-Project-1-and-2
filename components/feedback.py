import streamlit as st
from db import init_feedback_table, submit_feedback, get_all_feedback
from auth import has_role

# Ensure the feedback table is initialized
init_feedback_table()


def feedback():
    st.header("Feedback")

    # Role-based feedback functionality
    if has_role("student"):
        st.write("We value your feedback to enhance this learning assistant.")
        st.subheader("Submit Feedback (Anonymous)")
        feedback_text = st.text_area("Your Feedback", placeholder="Enter your feedback here...")
        if st.button("Submit Feedback"):
            if feedback_text.strip():
                submit_feedback(feedback_text)
                st.success("Thank you for your feedback! It has been submitted anonymously.")
            else:
                st.warning("Feedback cannot be empty.")

    elif has_role("teacher"):
        st.subheader("View Feedback")
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
