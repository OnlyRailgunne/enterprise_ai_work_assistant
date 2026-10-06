from app.project_service import (
    create_project as service_create_project,
    get_project as service_get_project,
    list_projects as service_list_projects,
    update_project as service_update_project,
)


def create_project(
    project_id,
    name,
    description=None,
    status="active",
):
    return service_create_project(
        project_id=project_id,
        name=name,
        description=description,
        status=status,
    )


def get_project(project_id):
    project = service_get_project(project_id)

    if project is None:
        return {
            "error": "Project not found",
        }

    return project


def list_projects(status=None):
    return service_list_projects(status=status)


def update_project(
    project_id,
    name=None,
    description=None,
    status=None,
):
    project = service_update_project(
        project_id=project_id,
        name=name,
        description=description,
        status=status,
    )

    if project is None:
        return {
            "error": "Project not found",
        }

    return project