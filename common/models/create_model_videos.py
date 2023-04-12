import sqlite3

conn = sqlite3.connect("database.db")
cursor = conn.cursor()

cursor.execute("drop table videos")

cursor.execute("""
CREATE TABLE videos (
video_code CHAR PRIMARY KEY,
video_url CHAR,
video_title CHAR,
video_thumbnail_path CHAR,
phrases CHAR,
meanings CHAR)
""")
               
conn.commit()
conn.close()