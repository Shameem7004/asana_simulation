import random
from utils.uuid import generate_uuid


TAG_POOL = [
    "urgent",
    "bug",
    "frontend",
    "backend",
    "customer-request",
    "blocked",
    "enhancement",
    "high-priority",
    "low-priority",
    "technical-debt"
]


def generate_tags(conn):
    cursor = conn.cursor()
    tag_ids = {}

    # Insert tags
    for tag in TAG_POOL:
        tag_id = generate_uuid()
        cursor.execute("""
            INSERT INTO tags (tag_id, name)
            VALUES (?, ?)
        """, (tag_id, tag))
        tag_ids[tag] = tag_id

    # Fetch tasks
    cursor.execute("SELECT task_id FROM tasks")
    tasks = [row[0] for row in cursor.fetchall()]

    for task_id in tasks:
        num_tags = random.randint(0, 4)
        selected_tags = random.sample(list(tag_ids.values()), num_tags)

        for tag_id in selected_tags:
            cursor.execute("""
                INSERT OR IGNORE INTO task_tags (task_id, tag_id)
                VALUES (?, ?)
            """, (task_id, tag_id))

    conn.commit()
