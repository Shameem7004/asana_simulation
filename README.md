# Asana Workspace Simulation

This project simulates a realistic Asana-like workspace for a mid-to-large B2B SaaS organization.
It generates structured, temporally consistent, and behaviorally realistic data for projects, tasks, users, teams, comments, custom fields, and tags using SQLite and Python.

The dataset is designed to support experimentation, analysis, and reinforcement-learning (RL) evaluation in enterprise project-management environments.

---

## ⚙️ Setup & Usage

### Prerequisites
- Python 3.8+

### Instructions

1.  **Clone the repository** (if you haven't already).

2.  **Create and activate a virtual environment:**
    ```bash
    # Navigate to the project root directory
    cd /path/to/asana_simulation

    # Create a virtual environment
    python3 -m venv venv

    # Activate it (macOS/Linux)
    source venv/bin/activate
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **(Optional) Configure the simulation:**
    Copy the example environment file and edit the values in `.env` to change the simulation parameters.
    ```bash
    cp .env.example .env
    ```

5.  **Generate the data:**
    The generation is a two-step process. Run the scripts from the project root directory.

    ```bash
    # 1. Create the database and its schema
    python src/createDb.py

    # 2. Populate the database with simulated data
    python src/main.py
    ```

    The generated database will be located at `output/asana_simulation.sqlite`.

---

## 📌 Features

- Realistic organizational hierarchy (organization → teams → projects → tasks)
- Workflow modeling using sections and task movement
- Subtasks using self-referential relationships
- Human-like collaboration via comments
- Flexible metadata using custom fields
- Cross-project categorization using tags
- Temporal and relational consistency enforced
- Modular, extensible codebase

---

## 🔧 Configuration

You can configure the simulation by creating a `.env` file in the project root. The following variables are available:

-   `DB_PATH`: The file path for the output SQLite database.
-   `ORG_NAME`: The name of the simulated organization.
-   `ORG_DOMAIN`: The domain for the simulated organization.
-   `TOTAL_USERS`: The number of users to generate (Note: other entity counts are derived from this).

---

## 🧱 Project Structure

```
asana_simulation/
├── .env.example
├── schema.sql
├── requirements.txt
├── src/
│   ├── main.py
│   ├── createDb.py
│   ├── config.py
│   ├── utils/
│   │   ├── db.py
│   │   ├── uuid.py
│   │   └── dates.py
│   └── generators/
│       ├── users.py
│       ├── teams.py
│       ├── projects.py
│       └── ... (and other generators)
└── output/
    └── asana_simulation.sqlite
```