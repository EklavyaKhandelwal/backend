from app import db
from datetime import datetime

# Define the TaskLogger model representing logs related to tasks
class TaskLogger(db.Model):
    __tablename__ = 'task_logger'  # Explicit table name in the database

    # Primary key column - unique identifier for each task log
    id = db.Column(db.Integer, primary_key=True)

    # Foreign key linking to TaskManager table; if the related task is deleted, this log is also deleted (CASCADE)
    task_id = db.Column(db.Integer, db.ForeignKey('task_manager.id', ondelete='CASCADE'))

    # Status of the task (e.g., pending, completed, failed)
    status = db.Column(db.String(20), default='pending')

    # Timestamp for when the log entry was created; defaults to current UTC time
    logged_date = db.Column(db.DateTime, default=datetime.utcnow)

    # Foreign key linking to the user who last updated the task log
    updated_by = db.Column(db.Integer, db.ForeignKey('users.id'))

    # Table index to optimize queries filtering by logged_date
    __table_args__ = (db.Index('idx_task_logger_date', 'logged_date'),)
