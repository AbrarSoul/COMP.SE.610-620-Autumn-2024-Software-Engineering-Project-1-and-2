import streamlit as st
import pandas as pd

def progress_tracking():
    st.header("Progress Tracking")
    st.subheader("Progress Map")

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
