from app import db

# Define the TaskManager model representing a task entity
class TaskManager(db.Model):
    __tablename__ = 'task_manager'  # Set the table name explicitly

    # Primary key - unique identifier for each task
    id = db.Column(db.Integer, primary_key=True)

    # Title of the task (required)
    title = db.Column(db.String(100), nullable=False)

    # Optional detailed description of the task
    description = db.Column(db.Text)

    # Boolean flag to indicate if the task is active (used for soft deletion)
    is_active = db.Column(db.Boolean, default=True)

    # Foreign key linking to the user who created the task
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'))

    # Index to speed up queries filtering by the is_active field
    __table_args__ = (db.Index('idx_task_manager_is_active', 'is_active'),)
