import os
from dotenv import load_dotenv

load_dotenv()

DB_PATH = os.getenv("DB_PATH", "output/asana_simulation.sqlite")

ORG_NAME = os.getenv("ORG_NAME", "Nimbus AI Inc.")
ORG_DOMAIN = os.getenv("ORG_DOMAIN", "nimbus.ai")

TOTAL_USERS = int(os.getenv("TOTAL_USERS", 100))