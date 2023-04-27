import sqlite3

conn = sqlite3.connect("database.db")
c = conn.cursor()

c.execute("""
ALTER TABLE videos RENAME COLUMN video_thumbnail_path TO video_thumbnail_url;
""")

"""
video_code	channel_url	video_url	video_title	video_thumbnail_path
video_code	phrase	meaning	phrase_id
"""



conn.commit()
conn.close()