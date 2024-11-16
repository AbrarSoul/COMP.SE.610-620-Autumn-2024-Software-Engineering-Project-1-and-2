import sqlite3

conn = sqlite3.connect('lecture_summaries.db')
cursor = conn.cursor()
cursor.execute("DELETE FROM lectures")  # This deletes all records in the table
conn.commit()
conn.close()

print("All records deleted from the lectures table.")
