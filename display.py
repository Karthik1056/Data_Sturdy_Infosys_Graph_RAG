import sqlite3
import json

conn = sqlite3.connect("research.db")
conn.row_factory = sqlite3.Row
cursor = conn.cursor()

cursor.execute("""
SELECT title, url, substr(content,1,500) as preview
FROM crawled_sources
LIMIT 3;
""")

rows = cursor.fetchall()

print(json.dumps([dict(r) for r in rows], indent=4))
