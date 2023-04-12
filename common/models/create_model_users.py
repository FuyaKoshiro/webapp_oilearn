import sqlite3

conn = sqlite3.connect("database.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE users (
user_id INTEGER,
video_code CHAR(100),
phrase_id CHAR(200),
date DATESTAMP)
""")

conn.commit()
conn.close()