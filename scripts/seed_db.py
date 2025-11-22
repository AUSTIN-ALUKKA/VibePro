"""Idempotent seed script to insert two sample enrollments for demo/mock-mode."""
import sqlite3
import uuid
from backend.app.db import get_conn, ensure_db


def seed():
    ensure_db()
    conn = get_conn()
    cur = conn.cursor()
    samples = [
        ("enroll-1", "Alice", b"voiceprint-alice"),
        ("enroll-2", "Bob", b"voiceprint-bob"),
    ]
    for eid, name, vp in samples:
        cur.execute("SELECT 1 FROM enrollments WHERE id=?", (eid,))
        if cur.fetchone():
            print(f"Enrollment {eid} exists, skipping")
            continue
        cur.execute("INSERT INTO enrollments (id, name, voiceprint) VALUES (?, ?, ?)", (eid, name, vp))
        print(f"Inserted {eid}")
    conn.commit()
    conn.close()


if __name__ == "__main__":
    seed()
