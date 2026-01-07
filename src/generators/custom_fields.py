import random
from utils.uuid import generate_uuid


ENGINEERING_FIELDS = [
    ("Priority", "enum", ["High", "Medium", "Low"]),
    ("Story Points", "number", [1, 2, 3, 5, 8])
]

MARKETING_FIELDS = [
    ("Campaign Channel", "enum", ["Email", "Social", "Paid"]),
    ("Budget", "number", None)
]


def generate_custom_fields(conn):
    cursor = conn.cursor()

    # Fetch projects
    cursor.execute("""
        SELECT project_id, project_type
        FROM projects
    """)
    projects = cursor.fetchall()

    for project_id, project_type in projects:

        if project_type.startswith("engineering"):
            fields = ENGINEERING_FIELDS
        elif project_type == "marketing_campaign":
            fields = MARKETING_FIELDS
        else:
            continue

        for field_name, field_type, possible_values in fields:
            field_id = generate_uuid()

            cursor.execute("""
                INSERT INTO custom_field_definitions (
                    field_id, project_id, name, field_type, created_at
                ) VALUES (?, ?, ?, ?, datetime('now'))
            """, (
                field_id,
                project_id,
                field_name,
                field_type
            ))

            # Fetch tasks for this project
            cursor.execute("""
                SELECT task_id
                FROM tasks
                WHERE project_id = ?
            """, (project_id,))
            task_ids = [row[0] for row in cursor.fetchall()]

            for task_id in task_ids:
                # Not all tasks get all fields
                if random.random() < 0.3:
                    continue

                value_id = generate_uuid()

                if field_type == "enum":
                    value_text = random.choice(possible_values)
                    value_number = None
                else:
                    value_text = None
                    value_number = random.randint(1000, 100000)

                cursor.execute("""
                    INSERT INTO custom_field_values (
                        value_id, field_id, task_id,
                        value_text, value_number
                    ) VALUES (?, ?, ?, ?, ?)
                """, (
                    value_id,
                    field_id,
                    task_id,
                    value_text,
                    value_number
                ))

    conn.commit()
