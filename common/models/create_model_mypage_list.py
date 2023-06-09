import sqlite3

conn = sqlite3.connect("database.db")
c = conn.cursor()

c.execute("""
CREATE TABLE mypage (
mypage_id INTEGER PRIMARY KEY,
user_id INTEGER,
video_code CHAR(50),
phrases CHAR(50),
meaning CHAR(50),
date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
FOREIGN KEY(user_id) REFERENCES users(user_id),
FOREIGN KEY(video_code) REFERENCES videos(video_code))
""")

conn.commit()

c.execute("""
INSERT INTO mypage (mypage_id, user_id, video_code, phrases, meaning, date) VALUES (?, ?, ?, ?, ?, ?)
""", (1, 1, 'test_video_id', 'test_phrase', "test_meaning", "test_time"))

conn.commit()
conn.close()