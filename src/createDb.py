import sqlite3
from pathlib import Path

from config import DB_PATH

def create_database():
    # Ensure output folder exists
    Path(DB_PATH).parent.mkdir(parents=True, exist_ok=True)

    # schema.sql is in the project root
    schema_path = Path(__file__).resolve().parent.parent / "schema.sql"
    if not schema_path.exists():
        raise FileNotFoundError(f"Schema file not found: {schema_path}")

    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON;")

    with open(schema_path, "r", encoding="utf-8") as f:
        conn.executescript(f.read())

    conn.close()
    print(f"Database initialized at: {DB_PATH}")

if __name__ == "__main__":
    create_database()