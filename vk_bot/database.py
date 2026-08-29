import sqlite3
from contextlib import contextmanager

from . import config


def init_db():
    with _connect() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS subscribers (
                user_id INTEGER PRIMARY KEY
            )
            """
        )


def remember_user(user_id: int):
    with _connect() as conn:
        conn.execute(
            "INSERT OR IGNORE INTO subscribers (user_id) VALUES (?)", (user_id,)
        )


def all_subscribers():
    with _connect() as conn:
        rows = conn.execute("SELECT user_id FROM subscribers").fetchall()
    return [row[0] for row in rows]


@contextmanager
def _connect():
    conn = sqlite3.connect(config.DB_PATH)
    try:
        yield conn
        conn.commit()
    finally:
        conn.close()
