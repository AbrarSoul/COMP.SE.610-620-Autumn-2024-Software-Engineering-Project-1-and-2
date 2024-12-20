import streamlit as st
import pandas as pd

def progress_tracking():
    st.markdown("<h1 style='color: #4CAF50;'>Progress Tracking</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='color: #362f2f; font-weight: bold;'>Progress Map</h3>", unsafe_allow_html=True)

    # Sample progress data
    progress_data = {
        "Topic": ["L1_introdcution", "L2_product value", "L3_vision_scope_stakeholders", "L4_types of req", "L5_elicitation techniques"],
        "Completion (%)": [75, 50, 40, 20, 10]
    }
    progress_df = pd.DataFrame(progress_data)
    
    # Display the data as a table
    st.table(progress_df)
    
    # Display the data as a line chart
    st.line_chart(progress_df.set_index("Topic"))
