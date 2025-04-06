from app import db

# Define the User model representing application users
class User(db.Model):
    __tablename__ = 'users'  # Explicit table name for the users table

    # Primary key - unique ID for each user
    id = db.Column(db.Integer, primary_key=True)

    # Username must be unique and is required (not nullable)
    username = db.Column(db.String(80), unique=True, nullable=False)

    # Password is required (stored as a hashed string, typically)
    password = db.Column(db.String(120), nullable=False)

    # Role of the user - default is 'user', can be 'admin' or other roles
    role = db.Column(db.String(20), default='user')

    # String representation for debugging/logging
    def __repr__(self):
        return f'<User {self.username}>'
