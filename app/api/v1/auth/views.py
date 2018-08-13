from flask import jsonify, request
from werkzeug.security import generate_password_hash, check_password_hash

from . import auth
from app.api.v1.auth.models import User

user = User()

@auth.route('/register', methods=['POST'])
def register_user():
    """Register a new user"""
    data = request.get_json()
    errors = {}
    # Check for details
    if not data['username'] or not data['email'] \
            or not data['password'] or not data['confirm_password']:
        errors['missing_details'] = "Enter username, email, password and confirm password to register"
     # Check for duplicate username entry
    if data['username'] in user.users:
        errors['username'] = "Username already exists. Try another one"
    # Check for duplicate email entry 
    for one_user in user.users.values():
        if one_user.get('email') == data['email']:
            errors['email'] = "Email already exists. Try another one"
    # Check if password and confirm password match
    if data['password'] != data['confirm_password']:
        errors['password'] = "Your passwords do not match. Try again"
    if errors:
        return jsonify(errors), 400
    user_id = len(user.users) + 1
    password = generate_password_hash(data['password'])
    confirm_password = generate_password_hash(data['confirm_password'])
    # Create user if everything is OK
    new_user = {"user_id":user_id, "username":data['username'], 
                "email":data['email'],
                "password":password, "confirm_password":confirm_password, "logged_in": False}
    user.users[data['username']] = new_user
    return jsonify({"message" : "User registered successfully", 
                                    "user_id": user_id}), 201

@auth.route('/users', methods=['GET'])
def get_all_users():
    """Get all registered users"""
    return jsonify(user.users), 200

@auth.route('/login', methods=['POST'])
def login():
    """
    User sign in
    """
    errors = {}
    message = {}
    data = request.get_json()
    # Check for missing username and password
    if not data['username'] or not data['password']:
        errors['missing_details'] = "Enter both username and password"
    
    for one_user in user.users.values():
        # Check if username exists
        if not one_user:
            errors["missing_user"] = "You do not have an account with the username. Please register"
        # Check if username does not match password
        if not check_password_hash(one_user.get('password'), data['password']):
            errors['authentication'] = "Your username and password do not match"
        # If password matches username then return success message
        if check_password_hash(one_user.get('password'), data['password']):
            message['success'] = "You have been logged in successfully"
    # Set logged_in to True for logged in user
    for logged_in_user in user.users.values():
        if logged_in_user.get('username') == data['username']:
            logged_in_user["logged_in"] = True
    if errors:
        return jsonify(errors)
    if message:
        return jsonify(message)
