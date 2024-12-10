import sqlite3
from datetime import datetime

DB_PATH = 'lecture_summaries.db'

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Create table for lecture summaries
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS lectures (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            upload_date TEXT,
            file_path TEXT
        )
    ''')

    # Create table for user authentication
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            role TEXT NOT NULL CHECK (role IN ('student', 'teacher'))
        )
    ''')

    conn.commit()
    conn.close()
    print("Database initialized successfully!")

def save_to_db(title, file_path):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO lectures (title, upload_date, file_path) VALUES (?, ?, ?)", 
                   (title, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), file_path))
    conn.commit()
    conn.close()

def get_lectures():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT id, title, upload_date, file_path FROM lectures")
    lectures = cursor.fetchall()
    conn.close()
    return lectures

def delete_from_db(lecture_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM lectures WHERE id = ?", (lecture_id,))
    conn.commit()
    conn.close()

# Register a new user
def register_user(email, password, role):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO users (email, password, role) VALUES (?, ?, ?)", (email, password, role))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

# Authenticate a user
def authenticate_user(email, password):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT id, role FROM users WHERE email = ? AND password = ?", (email, password))
    user = cursor.fetchone()
    conn.close()
    if user:
        return {"id": user[0], "role": user[1]}
    return None

# Get user role by user ID
def get_user_role(user_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT role FROM users WHERE id = ?", (user_id,))
    role = cursor.fetchone()
    conn.close()
    return role[0] if role else None

def init_feedback_table():
    """Initialize the feedback table in the database."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS feedback (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            feedback_text TEXT NOT NULL,
            submitted_at TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()
    print("Feedback table initialized successfully!")


def submit_feedback(feedback_text):
    """Insert anonymous feedback into the feedback table."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    init_feedback_table()
    cursor.execute("INSERT INTO feedback (feedback_text, submitted_at) VALUES (?, ?)",
                   (feedback_text, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    conn.commit()
    conn.close()
    print("Feedback submitted successfully!")


def get_all_feedback():
    """Retrieve all feedback from the feedback table."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    init_feedback_table()
    cursor.execute("SELECT feedback_text, submitted_at FROM feedback ORDER BY submitted_at DESC")
    feedback = cursor.fetchall()
    conn.close()
    return feedback

