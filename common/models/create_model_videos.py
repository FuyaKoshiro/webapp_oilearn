import sqlite3

conn = sqlite3.connect("database.db")
c = conn.cursor()

c.execute("drop table videos")
conn.commit()

c.execute("""
CREATE TABLE videos (
video_id INTEGER PRIMARY KEY,
channel_url CHAR(500),
title CHAR(500),
url CHAR(2083),
thumbnail CHAR(2083),
phrase CHAR(50),
meaning CHAR(50),
video_code CHAR(50))
""")

conn.commit()

c.execute("""
INSERT INTO videos (video_id, channel_url, title, url, thumbnail, phrase, meaning, video_code) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
""", (1, "test_channel_url", "test_title", 'test_url', 'test_thumbnail', "testphrase", "test_meaning", "test_video_code"))

conn.commit()
conn.close()