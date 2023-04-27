import sqlite3

conn = sqlite3.connect("database.db")
c = conn.cursor()

suffix = -1
count = 0

for i in range(100):
    if count % 10 == 0:
        suffix += 1
    formatted_suffix = "{:02d}".format(suffix)
    formatted_i = "{:02d}".format(i)

    print(f"count: {count}\nformatted_suffix: {formatted_suffix}\nformatted_i: {formatted_i}\n================")
    c.execute("""
    UPDATE videos
    SET channel_url = "test_channel_url_{}"
    WHERE video_code = "test_video_code_{}";
    """.format(formatted_suffix, formatted_i))
    count += 1

conn.commit()
conn.close()