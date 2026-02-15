import sqlite3
import json


DB_NAME = "research.db"


def init_db():

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS crawled_sources (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        query TEXT,
        angle TEXT,

        title TEXT,
        url TEXT UNIQUE,

        content TEXT,
        content_length INTEGER,

        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)

    conn.commit()
    conn.close()

    print("\n✅ Database initialized successfully.\n")


# ⭐ OPTIONAL — View stored data
def preview_data(limit=3):

    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute(f"""
    SELECT
        title,
        url,
        substr(content,1,500) as preview,
        content_length,
        created_at
    FROM crawled_sources
    ORDER BY id DESC
    LIMIT {limit};
    """)

    rows = cursor.fetchall()

    print(json.dumps([dict(r) for r in rows], indent=4))

    conn.close()


if __name__ == "__main__":

    init_db()

    # ⭐ comment this if you only want creation
    preview_data()
