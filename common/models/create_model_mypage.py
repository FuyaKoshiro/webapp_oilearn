import sqlite3

conn = sqlite3.connect("database.db")
cursor = conn.cursor()

user_ids = range(100)
mypage_names = [str(user_ids[i])+"_mypage" for i in user_ids]

for mypage_name in mypage_names:
    cursor.execute(f"""
    CREATE TABLE `{mypage_name}` (
    user_id INTEGER,
    video_code CHAR,
    phrase_id CHAR,
    date DATESTAMP)
    """)

conn.commit()
conn.close()