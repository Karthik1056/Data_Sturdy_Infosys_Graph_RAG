import sqlite3


def save_crawled_source(query, angle, title, url, content):

    conn = sqlite3.connect("research.db")
    cursor = conn.cursor()

    cursor.execute("""
        INSERT OR IGNORE INTO crawled_sources
        (query, angle, title, url, content, content_length)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        query,
        angle,
        title,
        url,
        content,
        len(content)
    ))

    conn.commit()
    conn.close()
