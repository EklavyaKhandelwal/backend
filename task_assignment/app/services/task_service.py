from app import db
from app.models.task_manager import TaskManager
from app.models.task_logger import TaskLogger

def create_task(title, description, user_id):
    """Create a new task."""

    # Instantiate a new TaskManager object with provided data
    task = TaskManager(title=title, description=description, created_by=user_id)

    # Add the new task to the session and save it to the database
    db.session.add(task)
    db.session.commit()

    return task

def update_task(task_id, user_id, title=None, description=None):
    """Update an existing task if authorized."""

    # Retrieve the task by ID or return a 404 error if not found
    task = TaskManager.query.get_or_404(task_id)

    # Check if the current user is authorized to update the task
    if task.created_by != user_id:
        raise PermissionError("Unauthorized")

    # Update the task title if a new one is provided
    if title:
        task.title = title

    # Update the task description if a new one is provided
    if description:
        task.description = description

    # Commit the changes to the database
    db.session.commit()

    return task
