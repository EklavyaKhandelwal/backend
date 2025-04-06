from app import db
from app.models.task_manager import TaskManager
from app.models.task_logger import TaskLogger

# Repository class to abstract and manage task-related database operations
class TaskRepository:

    @staticmethod
    def get_task_by_id(task_id):
        # Retrieve a single TaskManager entry by its ID
        return TaskManager.query.get(task_id)

    @staticmethod
    def get_tasks_paginated(page, per_page):
        # Return a paginated list of TaskLogger entries
        return TaskLogger.query.paginate(page=page, per_page=per_page)

    @staticmethod
    def get_tasks_by_date(date):
        # Retrieve all TaskLogger entries that match the specified date
        return TaskLogger.query.filter_by(logged_date=date).all()
