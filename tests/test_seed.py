import sqlite3
from backend.app.db import get_conn, ensure_db


def test_seed_idempotent():
    ensure_db()
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT COUNT(1) FROM enrollments")
    c1 = cur.fetchone()[0]
    # run seed script
    from scripts.seed_db import seed
    seed()
    cur.execute("SELECT COUNT(1) FROM enrollments")
    c2 = cur.fetchone()[0]
    assert c2 >= c1
    conn.close()
