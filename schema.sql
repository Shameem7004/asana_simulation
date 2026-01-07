PRAGMA foreign_keys = ON;

CREATE TABLE organizations (
    organization_id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    domain TEXT NOT NULL,
    created_at TIMESTAMP NOT NULL
);

CREATE TABLE users (
    user_id TEXT PRIMARY KEY,
    organization_id TEXT NOT NULL,
    full_name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    role TEXT NOT NULL,
    department TEXT NOT NULL,
    is_active INTEGER NOT NULL,
    created_at TIMESTAMP NOT NULL,
    FOREIGN KEY (organization_id) REFERENCES organizations(organization_id)
);


CREATE TABLE teams (
    team_id TEXT PRIMARY KEY,
    organization_id TEXT NOT NULL,
    name TEXT NOT NULL,
    created_at TIMESTAMP NOT NULL,
    FOREIGN KEY (organization_id) REFERENCES organizations(organization_id)
);


CREATE TABLE team_memberships (
    membership_id TEXT PRIMARY KEY,
    team_id TEXT NOT NULL,
    user_id TEXT NOT NULL,
    role TEXT NOT NULL,
    joined_at TIMESTAMP NOT NULL,
    FOREIGN KEY (team_id) REFERENCES teams(team_id),
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    UNIQUE (team_id, user_id)
);


CREATE TABLE projects (
    project_id TEXT PRIMARY KEY,
    team_id TEXT NOT NULL,
    name TEXT NOT NULL,
    project_type TEXT NOT NULL,
    start_date DATE,
    end_date DATE,
    created_at TIMESTAMP NOT NULL,
    FOREIGN KEY (team_id) REFERENCES teams(team_id)
);


CREATE TABLE sections (
    section_id TEXT PRIMARY KEY,
    project_id TEXT NOT NULL,
    name TEXT NOT NULL,
    position INTEGER NOT NULL,
    FOREIGN KEY (project_id) REFERENCES projects(project_id)
);


CREATE TABLE tasks (
    task_id TEXT PRIMARY KEY,
    project_id TEXT NOT NULL,
    section_id TEXT NOT NULL,
    parent_task_id TEXT,
    name TEXT NOT NULL,
    description TEXT,
    assignee_id TEXT,
    due_date DATE,
    completed INTEGER NOT NULL,
    created_at TIMESTAMP NOT NULL,
    completed_at TIMESTAMP,
    FOREIGN KEY (project_id) REFERENCES projects(project_id),
    FOREIGN KEY (section_id) REFERENCES sections(section_id),
    FOREIGN KEY (parent_task_id) REFERENCES tasks(task_id),
    FOREIGN KEY (assignee_id) REFERENCES users(user_id)
);


CREATE TABLE comments (
    comment_id TEXT PRIMARY KEY,
    task_id TEXT NOT NULL,
    user_id TEXT NOT NULL,
    content TEXT NOT NULL,
    created_at TIMESTAMP NOT NULL,
    FOREIGN KEY (task_id) REFERENCES tasks(task_id),
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);


CREATE TABLE custom_field_definitions (
    field_id TEXT PRIMARY KEY,
    project_id TEXT,
    name TEXT NOT NULL,
    field_type TEXT NOT NULL,
    created_at TIMESTAMP NOT NULL,
    FOREIGN KEY (project_id) REFERENCES projects(project_id)
);


CREATE TABLE custom_field_values (
    value_id TEXT PRIMARY KEY,
    field_id TEXT NOT NULL,
    task_id TEXT NOT NULL,
    value_text TEXT,
    value_number REAL,
    FOREIGN KEY (field_id) REFERENCES custom_field_definitions(field_id),
    FOREIGN KEY (task_id) REFERENCES tasks(task_id),
    UNIQUE (field_id, task_id)
);


CREATE TABLE tags (
    tag_id TEXT PRIMARY KEY,
    name TEXT NOT NULL UNIQUE
);


CREATE TABLE task_tags (
    task_id TEXT NOT NULL,
    tag_id TEXT NOT NULL,
    PRIMARY KEY (task_id, tag_id),
    FOREIGN KEY (task_id) REFERENCES tasks(task_id),
    FOREIGN KEY (tag_id) REFERENCES tags(tag_id)
);
