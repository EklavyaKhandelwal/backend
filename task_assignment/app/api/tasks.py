# Import necessary modules
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db, limiter
from app.models.task_manager import TaskManager
from app.models.task_logger import TaskLogger
from app.utils.validators import TaskSchema
from app.utils.cache import cache
from pydantic import ValidationError

# Create a Blueprint for task-related routes
tasks_bp = Blueprint('tasks', __name__)

# Route to handle CSV upload and load tasks into TaskManager
@tasks_bp.route('/upload-csv', methods=['POST'])
@jwt_required()  # Requires JWT token for access
@limiter.limit('10 per minute')  # Rate limit: max 10 requests per minute
def upload_csv():
    # Logic to parse and load tasks from a CSV file should be implemented here
    pass  # Placeholder

# Route to get paginated list of all tasks from TaskLogger
@tasks_bp.route('/tasks', methods=['GET'])
@jwt_required()
def get_tasks():
    # Get pagination parameters from query string
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)

    # Query tasks with pagination
    tasks = TaskLogger.query.paginate(page=page, per_page=per_page)

    # Return paginated task list and total count
    return jsonify({
        'tasks': [dict(id=t.id, task_id=t.task_id, status=t.status) for t in tasks.items],
        'total': tasks.total
    })

# Route to get tasks filtered by date (cached for 5 minutes)
@tasks_bp.route('/tasks', methods=['GET'])
@jwt_required()
@cache.cached(timeout=300, query_string=True)  # Cache based on query string for 5 minutes
def get_tasks_by_date():
    date = request.args.get('date')  # Get date from query parameters

    # Query tasks based on logged date
    tasks = TaskLogger.query.filter_by(logged_date=date).all()

    # Return list of tasks for the given date
    return jsonify([dict(id=t.id, task_id=t.task_id, status=t.status) for t in tasks])

# Route to get a single task by its TaskLogger ID
@tasks_bp.route('/task/<int:task_logger_id>', methods=['GET'])
@jwt_required()
def get_task(task_logger_id):
    # Fetch task or return 404 if not found
    task = TaskLogger.query.get_or_404(task_logger_id)

    # Return task details
    return jsonify(dict(id=task.id, task_id=task.task_id, status=task.status))

# Route to create a new task
@tasks_bp.route('/task', methods=['POST'])
@jwt_required()
def create_task():
    try:
        # Validate and parse request data using Pydantic schema
        data = TaskSchema(**request.json).dict()

        # Create TaskManager object with current user's identity
        task = TaskManager(**data, created_by=get_jwt_identity())

        # Add and commit task to database
        db.session.add(task)
        db.session.commit()

        return jsonify({'message': 'Task created'}), 201
    except ValidationError as e:
        # Return validation errors if input is invalid
        return jsonify(e.errors()), 400

# Route to update an existing task (only by its creator)
@tasks_bp.route('/task/<int:task_id>', methods=['PUT'])
@jwt_required()
def update_task(task_id):
    task = TaskManager.query.get_or_404(task_id)

    # Check if current user is the creator of the task
    if task.created_by != get_jwt_identity():
        return jsonify({'message': 'Unauthorized'}), 403

    # Update the task title (if provided)
    data = request.json
    task.title = data.get('title', task.title)

    # Commit changes to database
    db.session.commit()
    return jsonify({'message': 'Task updated'})

# Route to delete (soft delete) a task (only by its creator)
@tasks_bp.route('/task/<int:task_id>', methods=['DELETE'])
@jwt_required()
def delete_task(task_id):
    task = TaskManager.query.get_or_404(task_id)

    # Check if current user is the creator of the task
    if task.created_by != get_jwt_identity():
        return jsonify({'message': 'Unauthorized'}), 403

    # Mark task as inactive (soft delete)
    task.is_active = False
    db.session.commit()
    return jsonify({'message': 'Task deleted'})
