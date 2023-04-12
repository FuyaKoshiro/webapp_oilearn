import sqlite3

conn = sqlite3.connect("database.db")
cursor = conn.cursor()

cursor.execute("drop table users")

cursor.execute("""
CREATE TABLE users (
user_id INTEGER,
user_name CHAR,
user_email CHAR(200),
user_password CHAR)
""")

conn.commit()
conn.close()