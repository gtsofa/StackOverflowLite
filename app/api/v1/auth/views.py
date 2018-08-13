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
        return jsonify(errors)
    user_id = len(user.users) + 1
    password = generate_password_hash(data['password'])
    confirm_password = generate_password_hash(data['confirm_password'])
    # Create user if everything is OK
    new_user = {"user_id":user_id, "username":data['username'], 
                "email":data['email'],
                "password":password, "confirm_password":confirm_password}
    user.users[data['username']] = new_user
    return jsonify({"message" : "User registered successfully", 
                                    "user_id": user_id}), 201

@auth.route('/users', methods=['GET'])
def get_all_users():
    """Get all registered users"""
    return jsonify(user.users), 200