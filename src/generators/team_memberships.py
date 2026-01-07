import random
from utils.uuid import generate_uuid
from utils.dates import random_past_date

MEMBERSHIP_ROLES = [
    ("Member", 0.80),
    ("Senior Member", 0.15),
    ("Lead", 0.05),
]

def choose_role():
    roles, weights = zip(*MEMBERSHIP_ROLES)
    return random.choices(roles, weights)[0]

def teams_per_user():
    r = random.random()
    if r < 0.70:
        return 1
    elif r < 0.95:
        return 2
    else:
        return 3

def generate_team_memberships(conn, users, teams):
    cursor = conn.cursor()
    memberships = []

    for user_id in users:
        num_teams = teams_per_user()
        assigned_teams = random.sample(teams, num_teams)

        for team_id in assigned_teams:
            membership_id = generate_uuid()
            role = choose_role()
            joined_at = random_past_date(700)

            cursor.execute("""
                INSERT INTO team_memberships (
                    membership_id, team_id, user_id, role, joined_at
                ) VALUES (?, ?, ?, ?, ?)
            """, (
                membership_id, team_id, user_id, role, joined_at
            ))

            memberships.append(membership_id)

    conn.commit()
    return memberships
