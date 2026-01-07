import random
from datetime import timedelta

from utils.uuid import generate_uuid
from utils.dates import random_past_date

PROJECT_TYPES = [
    ("engineering_sprint", 0.45),
    ("bug_tracking", 0.15),
    ("marketing_campaign", 0.15),
    ("operations", 0.15),
    ("product_launch", 0.10),
]

def choose_project_type():
    types, weights = zip(*PROJECT_TYPES)
    return random.choices(types, weights)[0]

def generate_projects(conn, teams):
    cursor = conn.cursor()
    projects = []

    for team_id in teams:
        num_projects = random.randint(4, 12)

        for _ in range(num_projects):
            project_id = generate_uuid()
            ptype = choose_project_type()
            created_at = random_past_date(180)
            start_date = created_at.date()

            if ptype == "engineering_sprint":
                end_date = start_date + timedelta(days=14)
            elif ptype == "marketing_campaign":
                end_date = start_date + timedelta(days=random.randint(30, 90))
            else:
                end_date = None

            cursor.execute("""
                INSERT INTO projects (
                    project_id, team_id, name, project_type,
                    start_date, end_date, created_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                project_id, team_id,
                f"{ptype.replace('_', ' ').title()} Project",
                ptype, start_date, end_date, created_at
            ))

            projects.append(project_id)

    conn.commit()
    return projects
