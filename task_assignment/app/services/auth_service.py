from app import db
from app.models.user import User

def register_user(username, password, role='user'):
    """Register a new user."""
    
    # Check if the username already exists in the database
    if User.query.filter_by(username=username).first():
        raise ValueError("Username already exists")
    
    # Create a new User object (Note: Password should be hashed in production)
    user = User(username=username, password=password, role=role)
    
    # Add the new user to the database session and commit
    db.session.add(user)
    db.session.commit()
    
    return user

def login_user(username, password):
    """Authenticate a user."""
    
    # Find the user by username
    user = User.query.filter_by(username=username).first()
    
    # Verify password (Note: Should use hashed password comparison in production)
    if user and user.password == password:
        return user
    
    return None
