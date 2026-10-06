ALTER TABLE tasks
ADD COLUMN IF NOT EXISTS project_id INTEGER;

ALTER TABLE tasks
ADD CONSTRAINT tasks_project_id_fkey
FOREIGN KEY (project_id)
REFERENCES projects(id);