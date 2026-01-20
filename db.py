import os
import sqlite3
from datetime import datetime, timezone

DB_PATH = os.getenv("SQLITE_PATH", "reports.db")


def _connect():
    # Open a new connection per call (simple + safe for FastAPI threads)
    return sqlite3.connect(DB_PATH)


def init_db():
    with _connect() as con:
        con.execute(
            """
            CREATE TABLE IF NOT EXISTS reports (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                created_at TEXT NOT NULL,
                report TEXT NOT NULL
            )
            """
        )
        con.commit()


def save_report(report: str) -> int:
    created_at = datetime.now(timezone.utc).isoformat()
    with _connect() as con:
        cur = con.execute(
            "INSERT INTO reports (created_at, report) VALUES (?, ?)",
            (created_at, report),
        )
        con.commit()
        return int(cur.lastrowid)


def get_latest_report():
    with _connect() as con:
        cur = con.execute(
            "SELECT id, created_at, report FROM reports ORDER BY id DESC LIMIT 1"
        )
        row = cur.fetchone()
        if not row:
            return None
        return {"id": row[0], "created_at": row[1], "report": row[2]}


def get_history(limit: int = 50):
    limit = max(1, min(int(limit), 500))
    with _connect() as con:
        cur = con.execute(
            "SELECT id, created_at, report FROM reports ORDER BY id DESC LIMIT ?",
            (limit,),
        )
        rows = cur.fetchall()
        return [{"id": r[0], "created_at": r[1], "report": r[2]} for r in rows]