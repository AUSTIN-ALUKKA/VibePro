import sqlite3
import os
from typing import Optional
from .config import settings


def get_db_path() -> str:
    # For demo, default to sqlite path
    return settings.SQLITE_PATH


def ensure_db():
    path = get_db_path()
    dirpath = os.path.dirname(path)
    if dirpath and not os.path.exists(dirpath):
        os.makedirs(dirpath, exist_ok=True)

    conn = sqlite3.connect(path)
    cur = conn.cursor()
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS enrollments (
            id TEXT PRIMARY KEY,
            name TEXT,
            voiceprint BLOB
        )
        """
    )
    conn.commit()
    conn.close()


def get_conn() -> sqlite3.Connection:
    ensure_db()
    return sqlite3.connect(get_db_path(), check_same_thread=False)
