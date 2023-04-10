import sqlite3

conn = sqlite3.connect("database.db")
c = conn.cursor()

c.execute("""
CREATE TABLE videos (
video_id INTEGER PRIMARY KEY,
title CHAR(500),
url CHAR(2083),
thumbnail CHAR(2083),
phrase CHAR(50),
meaning CHAR(50))
""")

conn.commit()

c.execute("""
INSERT INTO videos (video_id, title, url, thumbnail, phrase, meaning) VALUES (?, ?, ?, ?, ?, ?)
""", (1, "test_title", 'test_url', 'test_thumbnail', "testphrase", "test_meaning"))

conn.commit()
conn.close()