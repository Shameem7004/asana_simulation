import random
from utils.uuid import generate_uuid
from utils.dates import random_past_date

TEAM_NAME_TEMPLATES = [
    "Payments Backend",
    "Search Infrastructure",
    "Growth Analytics",
    "Platform Reliability",
    "Content Marketing",
    "Customer Operations",
]

def generate_teams(conn, organization_id, count=450):
    cursor = conn.cursor()
    teams = []

    for i in range(count):
        team_id = generate_uuid()
        name = random.choice(TEAM_NAME_TEMPLATES) + f" {i}"
        created_at = random_past_date(900)

        cursor.execute("""
            INSERT INTO teams (
                team_id, organization_id, name, created_at
            ) VALUES (?, ?, ?, ?)
        """, (
            team_id, organization_id, name, created_at
        ))

        teams.append(team_id)

    conn.commit()
    return teams
