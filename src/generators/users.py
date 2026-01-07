from faker import Faker
import random

from utils.uuid import generate_uuid
from utils.dates import random_past_date

fake = Faker()

DEPARTMENTS = [
    ("Engineering", 0.45),
    ("Product", 0.15),
    ("Marketing", 0.15),
    ("Operations", 0.15),
    ("Leadership", 0.10),
]

ROLES_BY_DEPT = {
    "Engineering": ["Backend Engineer", "Frontend Engineer", "QA Engineer"],
    "Product": ["Product Manager", "Product Analyst"],
    "Marketing": ["Growth Manager", "Content Strategist"],
    "Operations": ["Ops Analyst", "Program Manager"],
    "Leadership": ["Director", "VP"],
}

def choose_department():
    depts, weights = zip(*DEPARTMENTS)
    return random.choices(depts, weights)[0]

def generate_users(conn, organization_id, count=7500):
    cursor = conn.cursor()
    users = []
    generated_emails = set()

    for _ in range(count):
        user_id = generate_uuid()
        
        # Ensure email is unique before proceeding
        while True:
            name = fake.name()
            email = name.lower().replace(" ", ".") + "@company.com"
            if email not in generated_emails:
                generated_emails.add(email)
                break
            # If email exists, loop again to generate a new one

        dept = choose_department()
        role = random.choice(ROLES_BY_DEPT[dept])

        is_active = 1 if random.random() < 0.85 else 0
        created_at = random_past_date(1000)

        cursor.execute("""
            INSERT INTO users (
                user_id, organization_id, full_name, email,
                role, department, is_active, created_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            user_id, organization_id, name, email,
            role, dept, is_active, created_at
        ))

        users.append(user_id)

    conn.commit()
    return users
