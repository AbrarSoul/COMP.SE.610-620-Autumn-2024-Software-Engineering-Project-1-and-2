import streamlit as st

def feedback():
    st.header("Feedback")
    st.write("We value your feedback to enhance this learning assistant.")
    
    # Feedback form
    feedback_text = st.text_area("Your Feedback", "Enter your feedback here...")
    if st.button("Submit Feedback"):
        st.write("Thank you for your feedback!")
