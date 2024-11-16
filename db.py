import sqlite3
from datetime import datetime

DB_PATH = 'lecture_summaries.db'

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS lectures (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        title TEXT,
                        upload_date TEXT,
                        file_path TEXT
                    )''')
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



