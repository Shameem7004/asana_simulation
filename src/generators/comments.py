import random
from datetime import timedelta, datetime

from utils.uuid import generate_uuid
from utils.dates import random_workday_date


COMMENT_TEMPLATES = [
    "Please review this when you get a chance.",
    "This is blocked due to dependency.",
    "I have completed my part.",
    "Waiting for approval.",
    "Can someone take a look?",
    "This looks good to me.",
    "Pushing this to the next sprint."
]


def generate_comments(conn):
    cursor = conn.cursor()

    # Fetch tasks with creation time
    cursor.execute("""
        SELECT task_id, created_at
        FROM tasks
    """)
    tasks = cursor.fetchall()

    # Fetch all users
    cursor.execute("SELECT user_id FROM users")
    users = [row[0] for row in cursor.fetchall()]

    for task_id, task_created_at_str in tasks:
        num_comments = random.randint(0, 8)
        
        # Convert the string from the DB back to a datetime object
        task_created_at = datetime.fromisoformat(task_created_at_str)

        for _ in range(num_comments):
            comment_id = generate_uuid()
            user_id = random.choice(users)
            content = random.choice(COMMENT_TEMPLATES)

            created_at = task_created_at + timedelta(
                days=random.randint(0, 10)
            )

            cursor.execute("""
                INSERT INTO comments (
                    comment_id, task_id, user_id, content, created_at
                ) VALUES (?, ?, ?, ?, ?)
            """, (
                comment_id,
                task_id,
                user_id,
                content,
                created_at
            ))

    conn.commit()
