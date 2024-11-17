#!/bin/bash

# Activate the virtual environment
source venv/bin/activate  # Adjust this if your venv is named differently

# Install the required dependencies
pip install -r requirements.txt

# Run the Streamlit app
streamlit run app.py
