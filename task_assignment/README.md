# Task Assignment Backend

## Setup
1. Clone the repository: `git clone <repo-url>`
2. Install dependencies: `pip install -r requirements.txt`
3. Set up environment variables in `.env`
4. Run Docker: `docker-compose up --build`

## API Endpoints
- `POST /api/upload-csv`: Upload CSV to TaskManager
- `GET /api/tasks`: Paginated list of tasks
- `GET /api/tasks?date=<date>`: Tasks by date
- `GET /api/task/<id>`: Task details
- `POST /api/task`: Create task
- `PUT /api/task/<id>`: Update task
- `DELETE /api/task/<id>`: Soft delete task

## Architecture
- **Blueprints**: Modular API endpoints
- **Services**: Business logic
- **Repositories**: Database operations
- **Models**: SQLAlchemy ORM
- **Celery**: Background tasks