import pytest
from app import create_app, db

@pytest.fixture
def app():
    app = create_app()
    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

def test_get_tasks(client):
    response = client.get('/api/tasks')
    assert response.status_code == 401  # Unauthorized without JWT