import sqlite3

conn = sqlite3.connect("database.db")
c = conn.cursor()

c.execute("""
delete from videos
where video_code like "test_%" """)

conn.commit()
conn.close()