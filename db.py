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
            student_id TEXT UNIQUE,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            role TEXT NOT NULL CHECK (role IN ('student', 'teacher'))
        )
    ''')

    conn.commit()
    conn.close()

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
def register_user(email, password, role, student_id=None):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    try:
        if role == "student" and student_id:
            cursor.execute("INSERT INTO users (email, password, role, student_id) VALUES (?, ?, ?, ?)",
                           (email, password, role, student_id))
        else:
            cursor.execute("INSERT INTO users (email, password, role) VALUES (?, ?, ?)",
                           (email, password, role))
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

def init_quiz_results_table():
    """Initialize the quiz results table in the database."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS quiz_results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER NOT NULL,
            lecture_name TEXT NOT NULL,
            difficulty TEXT NOT NULL,
            score INTEGER NOT NULL,
            total_questions INTEGER NOT NULL,
            submitted_at TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()


def save_quiz_result(student_id, lecture_name, difficulty, score, total_questions):
    """
    Save a student's quiz result into the database.

    Args:
        student_id (int): ID of the student.
        lecture_name (str): Name of the lecture PDF.
        difficulty (str): Difficulty level of the quiz.
        score (int): Student's score.
        total_questions (int): Total number of questions in the quiz.
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO quiz_results (student_id, lecture_name, difficulty, score, total_questions, submitted_at)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (student_id, lecture_name, difficulty, score, total_questions, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    conn.commit()
    conn.close()


def get_student_quiz_results(student_id):
    """
    Retrieve quiz results for a specific student.

    Args:
        student_id (int): ID of the student.

    Returns:
        list[tuple]: List of quiz results.
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        SELECT lecture_name, difficulty, score, total_questions, submitted_at
        FROM quiz_results
        WHERE student_id = ?
        ORDER BY submitted_at DESC
    ''', (student_id,))
    results = cursor.fetchall()
    conn.close()
    return results

def get_filtered_quiz_results(student_id=None, email=None):
    """
    Retrieve quiz results based on filters.

    Args:
        student_id (str): Filter by student ID.
        email (str): Filter by email.

    Returns:
        list[tuple]: Filtered quiz results.
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    query = '''
        SELECT u.student_id, u.email, q.lecture_name, q.difficulty, q.score, q.total_questions, q.submitted_at
        FROM quiz_results q
        JOIN users u ON q.student_id = u.student_id
    '''
    params = []

    # Apply filters dynamically
    if student_id:
        query += " WHERE u.student_id = ?"
        params.append(student_id)
    elif email:
        query += " WHERE u.email = ?"
        params.append(email)

    query += " ORDER BY q.submitted_at DESC"
    cursor.execute(query, tuple(params))
    results = cursor.fetchall()
    conn.close()
    return results

def get_all_quiz_results():
    """
    Retrieve all quiz results (for teacher viewing).

    Returns:
        list[tuple]: List of all quiz results.
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        SELECT student_id, lecture_name, difficulty, score, total_questions, submitted_at
        FROM quiz_results
        ORDER BY submitted_at DESC
    ''')
    results = cursor.fetchall()
    conn.close()
    return results

def init_assignments_table():
    """Initialize the assignments table."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS assignments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id TEXT,
            student_name TEXT,
            assignment_title TEXT NOT NULL,
            generated_assignment TEXT,  -- Allow NULL for this column
            submitted_file_path TEXT
        )
    ''')
    conn.commit()
    conn.close()

def save_generated_assignment(assignment_title, generated_assignment):
    """Save the generated assignment text to the database."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO assignments (assignment_title, generated_assignment)
        VALUES (?, ?)
    ''', (assignment_title, generated_assignment))
    conn.commit()
    conn.close()


def submit_student_assignment(student_id, student_name, assignment_title, file_path):
    """Save the student-submitted assignment PDF to the database."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO assignments (student_id, student_name, assignment_title, submitted_file_path)
        VALUES (?, ?, ?, ?)
    ''', (student_id, student_name, assignment_title, file_path))
    conn.commit()
    conn.close()


def get_all_assignments():
    """Fetch all submitted assignments (for teachers)."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        SELECT id, student_name, assignment_title, generated_assignment, submitted_file_path
        FROM assignments
    ''')
    assignments = cursor.fetchall()
    conn.close()
    return assignments


def get_student_assignments(student_id):
    """Fetch assignments for a specific student."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        SELECT assignment_title, generated_assignment, submitted_file_path
        FROM assignments
        WHERE student_id = ?
    ''', (student_id,))
    assignments = cursor.fetchall()
    conn.close()
    return assignments

def init_database():
    """Initialize all required tables."""
    init_db()
    init_quiz_results_table()
    init_assignments_table()
    print("Database tables initialized successfully!")
    