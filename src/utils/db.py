import sqlite3
from pathlib import Path

from config import DB_PATH

def get_connection():
    db_path = Path(DB_PATH)
    db_path.parent.mkdir(parents=True, exist_ok=True)

    conn = sqlite3.connect(db_path)
    conn.execute("PRAGMA foreign_keys = ON;")

    # Fail fast if schema wasn't initialized
    row = conn.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name='organizations'"
    ).fetchone()
    if row is None:
        raise RuntimeError(
            f"Database schema not found in {db_path}. Run: python src/createDb.py"
        )

    return conn
