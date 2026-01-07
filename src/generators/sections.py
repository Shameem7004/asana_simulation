from utils.uuid import generate_uuid

SECTION_TEMPLATES = {
    "engineering_sprint": [
        "Backlog",
        "In Progress",
        "Code Review",
        "Done"
    ],
    "bug_tracking": [
        "Open",
        "Investigating",
        "Fixing",
        "Resolved"
    ],
    "marketing_campaign": [
        "Ideation",
        "Content",
        "Review",
        "Published"
    ],
    "operations": [
        "To Do",
        "In Progress",
        "Blocked",
        "Completed"
    ],
    "product_launch": [
        "Planning",
        "Execution",
        "Validation",
        "Launched"
    ]
}

def generate_sections(conn):
    cursor = conn.cursor()
    sections = {}

    cursor.execute("SELECT project_id, project_type FROM projects")
    projects = cursor.fetchall()

    for project_id, project_type in projects:
        template = SECTION_TEMPLATES.get(project_type, ["To Do", "Done"])
        sections[project_id] = []

        for position, name in enumerate(template, start=1):
            section_id = generate_uuid()

            cursor.execute("""
                INSERT INTO sections (
                    section_id, project_id, name, position
                ) VALUES (?, ?, ?, ?)
            """, (
                section_id, project_id, name, position
            ))

            sections[project_id].append(section_id)

    conn.commit()
    return sections
