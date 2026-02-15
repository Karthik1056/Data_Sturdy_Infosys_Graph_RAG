from fastapi import APIRouter
import sqlite3

router = APIRouter()

DB_NAME = "research.db"


@router.get("/sources")
def get_sources(limit: int = 20):

    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            id,
            query,
            angle,
            title,
            url,
            substr(content,1,500) as preview,
            content_length,
            created_at
        FROM crawled_sources
        ORDER BY id DESC
        LIMIT ?
    """, (limit,))

    rows = cursor.fetchall()
    conn.close()

    return [dict(r) for r in rows]
