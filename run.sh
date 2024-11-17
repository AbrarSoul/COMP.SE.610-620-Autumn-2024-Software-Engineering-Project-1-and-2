#!/bin/bash

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Virtual environment not found. Creating one..."
    python3 -m venv venv  # Create a new virtual environment
fi

# Activate the virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install required dependencies
echo "Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Initialize the database
echo "Initializing the database..."
python3 -c "import db; db.init_db()"

# Run the Streamlit app
echo "Starting the Streamlit app..."
streamlit run app.py
