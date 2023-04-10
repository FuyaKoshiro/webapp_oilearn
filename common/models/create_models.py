import sqlite3

conn = sqlite3.connect("database.db")
c = conn.cursor()

c.execute("""
CREATE TABLE users (
id INTEGER PRIMARY KEY AUTOINCREMENT,
username CHAR(50),
email CHAR(50),
password CHAR(50))
""")

conn.commit()

c.execute("""
INSERT INTO users (username, email, password) VALUES (?, ?, ?)
""", ('test_user', 'test_email', 'test_pass'))

conn.commit()
conn.close()