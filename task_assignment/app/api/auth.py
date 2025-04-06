# Import necessary modules from Flask and JWT
from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token

# Import database instance, user model, and authentication service functions
from app import db
from app.models.user import User
from app.services.auth_service import register_user, login_user

# Create a Blueprint for authentication-related routes
auth_bp = Blueprint('auth', __name__)

# Route to handle user registration
@auth_bp.route('/register', methods=['POST'])
def register():
    # Get the JSON data from the request body
    data = request.json

    # Call the register_user service function with username, password, and optional role
    user = register_user(data['username'], data['password'], data.get('role', 'user'))

    # Return a success message with HTTP 201 status (Created)
    return jsonify({'message': 'User registered'}), 201

# Route to handle user login
@auth_bp.route('/login', methods=['POST'])
def login():
    # Get the JSON data from the request body
    data = request.json

    # Call the login_user service function to validate credentials
    user = login_user(data['username'], data['password'])

    # If credentials are valid, create a JWT token with user's ID as identity
    if user:
        token = create_access_token(identity=user.id)
        return jsonify({'token': token})
    
    # If credentials are invalid, return an error message with HTTP 401 status (Unauthorized)
    return jsonify({'message': 'Invalid credentials'}), 401
