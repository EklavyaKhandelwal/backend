from app import celery, db
from app.models.task_manager import TaskManager
from app.models.task_logger import TaskLogger
from datetime import datetime

@celery.task
def daily_task_loader():
    """Background task to log active tasks daily."""

    # Get the current UTC date (without time)
    today = datetime.utcnow().date()

    # Retrieve all tasks that are currently active
    active_tasks = TaskManager.query.filter_by(is_active=True).all()

    # Iterate through each active task
    for task in active_tasks:
        # Check if a log entry already exists for this task for today
        existing_log = TaskLogger.query.filter_by(task_id=task.id, logged_date=today).first()

        # If no log exists, create a new TaskLogger entry
        if not existing_log:
            log = TaskLogger(task_id=task.id)
            db.session.add(log)

    # Commit all new log entries to the database
    db.session.commit()
