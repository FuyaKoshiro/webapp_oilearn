import sqlite3

conn = sqlite3.connect("database.db")
c = conn.cursor()

c.execute("""
SELECT name FROM sqlite_master WHERE type="table" AND name LIKE "video_test%"
""")

table_name = c.fetchall()
table_name = [name[0] for name in table_name]
conn.close()

print(table_name)

for name in table_name:
    conn = sqlite3.connect("database.db")
    c = conn.cursor()

    c.execute("""
    DROP table {}
    """.format(name))
    conn.close()