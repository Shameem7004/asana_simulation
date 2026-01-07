from utils.db import get_connection
from utils.uuid import generate_uuid

from config import ORG_NAME, ORG_DOMAIN, TOTAL_USERS

from generators.users import generate_users
from generators.teams import generate_teams
from generators.team_memberships import generate_team_memberships
from generators.projects import generate_projects
from generators.sections import generate_sections
from generators.tasks import generate_tasks
from generators.comments import generate_comments
from generators.custom_fields import generate_custom_fields
from generators.tags import generate_tags


def main():
    conn = get_connection()
    cursor = conn.cursor()

    organization_id = generate_uuid()
    cursor.execute("""
        INSERT INTO organizations (
            organization_id, name, domain, created_at
        ) VALUES (?, ?, ?, datetime('now'))
    """, (
        organization_id,
        ORG_NAME,
        ORG_DOMAIN
    ))
    conn.commit()

    print("Generating users...")
    users = generate_users(conn, organization_id, TOTAL_USERS)

    print("Generating teams...")
    teams = generate_teams(conn, organization_id)

    print("Generating team memberships...")
    generate_team_memberships(conn, users, teams)

    print("Generating projects...")
    generate_projects(conn, teams)

    print("Generating sections...")
    generate_sections(conn)

    print("Generating tasks & subtasks...")
    generate_tasks(conn)

    print("Generating comments...")
    generate_comments(conn)

    print("Generating custom fields...")
    generate_custom_fields(conn)

    print("Generating tags...")
    generate_tags(conn)

    conn.close()


if __name__ == "__main__":
    main()
