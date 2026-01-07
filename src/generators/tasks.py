import random
from datetime import timedelta

from utils.uuid import generate_uuid
from utils.dates import random_workday_date


# -----------------------------
# Task name templates
# -----------------------------

ENGINEERING_TASKS = [
    "Refactor authentication logic",
    "Fix API timeout issue",
    "Implement pagination support",
    "Optimize database queries",
    "Add unit tests for service",
    "Improve error handling",
    "Update API documentation"
]

MARKETING_TASKS = [
    "Draft campaign email copy",
    "Design landing page assets",
    "Schedule social media posts",
    "Analyze campaign performance",
    "Coordinate influencer outreach"
]

OPERATIONS_TASKS = [
    "Prepare weekly operations report",
    "Update onboarding checklist",
    "Audit compliance documents",
    "Coordinate vendor follow-up",
    "Review SLA metrics"
]


# -----------------------------
# Task count by project type
# -----------------------------

TASK_COUNT_BY_TYPE = {
    "engineering_sprint": (40, 120),
    "bug_tracking": (30, 80),
    "marketing_campaign": (20, 60),
    "operations": (10, 40),
    "product_launch": (25, 70)
}


# -----------------------------
# Helper functions
# -----------------------------

def completion_rate(project_type):
    if project_type == "engineering_sprint":
        return random.uniform(0.70, 0.85)
    elif project_type == "bug_tracking":
        return random.uniform(0.60, 0.70)
    elif project_type == "operations":
        return random.uniform(0.40, 0.50)
    else:
        return 0.60


def generate_due_date(created_at):
    r = random.random()

    if r < 0.10:
        return None
    elif r < 0.35:
        return created_at + timedelta(days=random.randint(1, 7))
    elif r < 0.75:
        return created_at + timedelta(days=random.randint(8, 30))
    elif r < 0.95:
        return created_at + timedelta(days=random.randint(31, 90))
    else:
        # overdue task
        return created_at - timedelta(days=random.randint(1, 5))


def choose_task_name(project_type):
    if project_type.startswith("engineering"):
        return random.choice(ENGINEERING_TASKS)
    elif project_type == "marketing_campaign":
        return random.choice(MARKETING_TASKS)
    else:
        return random.choice(OPERATIONS_TASKS)


# -----------------------------
# Subtasks generator
# -----------------------------

def generate_subtasks(
    cursor,
    project_id,
    section_id,
    parent_task_id,
    assignee_id,
    parent_created_at
):
    num_subtasks = random.randint(1, 5)

    for _ in range(num_subtasks):
        subtask_id = generate_uuid()
        created_at = parent_created_at + timedelta(days=random.randint(1, 3))

        cursor.execute("""
            INSERT INTO tasks (
                task_id, project_id, section_id, parent_task_id,
                name, description, assignee_id,
                due_date, completed, created_at, completed_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            subtask_id,
            project_id,
            section_id,
            parent_task_id,
            "Subtask: " + random.choice(ENGINEERING_TASKS),
            None,
            assignee_id,
            None,
            0,
            created_at,
            None
        ))


# -----------------------------
# Main tasks generator
# -----------------------------

def generate_tasks(conn):
    cursor = conn.cursor()
    all_tasks = []

    # Fetch projects
    cursor.execute("""
        SELECT project_id, team_id, project_type
        FROM projects
    """)
    projects = cursor.fetchall()

    for project_id, team_id, project_type in projects:

        min_tasks, max_tasks = TASK_COUNT_BY_TYPE.get(
            project_type, (20, 50)
        )
        num_tasks = random.randint(min_tasks, max_tasks)

        # Fetch sections for the project
        cursor.execute("""
            SELECT section_id
            FROM sections
            WHERE project_id = ?
            ORDER BY position
        """, (project_id,))
        section_ids = [row[0] for row in cursor.fetchall()]

        if not section_ids:
            continue

        # Fetch team members (valid assignees)
        cursor.execute("""
            SELECT user_id
            FROM team_memberships
            WHERE team_id = ?
        """, (team_id,))
        team_users = [row[0] for row in cursor.fetchall()]

        for _ in range(num_tasks):
            task_id = generate_uuid()
            section_id = random.choice(section_ids)
            created_at = random_workday_date(180)

            name = choose_task_name(project_type)

            # Assignment logic
            if random.random() < 0.15 or not team_users:
                assignee_id = None
            else:
                assignee_id = random.choice(team_users)

            # Completion logic
            completed = 1 if random.random() < completion_rate(project_type) else 0
            completed_at = None

            if completed:
                completed_at = created_at + timedelta(
                    days=random.randint(1, 14)
                )

            due_date = generate_due_date(created_at)

            cursor.execute("""
                INSERT INTO tasks (
                    task_id, project_id, section_id, parent_task_id,
                    name, description, assignee_id,
                    due_date, completed, created_at, completed_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                task_id,
                project_id,
                section_id,
                None,
                name,
                None,
                assignee_id,
                due_date,
                completed,
                created_at,
                completed_at
            ))

            all_tasks.append(task_id)

            # Generate subtasks (~30%)
            if random.random() < 0.30:
                generate_subtasks(
                    cursor,
                    project_id,
                    section_id,
                    task_id,
                    assignee_id,
                    created_at
                )

    conn.commit()
    return all_tasks
