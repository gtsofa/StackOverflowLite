import os
import re
import jwt
import datetime
from functools import wraps
from flask import request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash

from . import auth_v2 
from app.api.v2.models import User
from app.config import conn

cur = conn.cursor()

def valid_username(username):
    if re.match(r'^[a-zA-Z0-9]{5,20}$', username):
        return True
    return False

def valid_email_address(email):
    if re.match(r'^[a-zA-Z0-9_\-\.]{3,}@.*\.[a-z]{2,4}$', email):
        return True
    return False



def auth_required(fn):
    """
    This is required for authentication
    """
    @wraps(fn)
    def decorated(*args, **kwargs):
        users = User.get_users(cur)
        token = None
        user = {}
        if "x-access-token" in request.headers:
            token = request.headers["x-access-token"]
        if not token:
            return jsonify({"message":"Token is missing"}), 401
        try:
            data = jwt.decode(token, os.getenv("SECRET"))
            for one_user in users:
                if one_user["username"] == data["username"]:
                    user = one_user
            current_user = user
        except:
            return jsonify({"message":"Token is invalid"}), 401
        return fn(current_user, *args, **kwargs)
    return decorated


@auth_v2.route("/register", methods=["POST"])
def register_user():
    """
    Register a user
    """
    
    try:
        data = request.get_json()
        errors = {}
        # check for details
        if not data['username'] or not data['email'] or not data['password'] or not data['confirm_password']:
            errors["missing_details"] = "Enter username, email, password and confirm_password to register"
        if data["password"] != data["confirm_password"]:
            errors['missmatched password'] = "Password and confirm password must match to register"
        # check for duplicate username entry
        users = User.get_users(cur)
        for user in users:
            if user["username"] == data["username"]:
                errors["duplicate_username"] = "Username already exists. Try another one!"
            if user["email"] == data["email"]:
                errors["duplicate_email"] = "Email already exists. Try another one"
        if errors:
            return jsonify(errors), 400
        password = generate_password_hash(data["password"])
        confirm_password = generate_password_hash(data["confirm_password"])
        User.create_user(cur, data["username"], data["email"], password, confirm_password)
        return jsonify({"message":"User registered successfully"}), 201
    except(ValueError, KeyError, TypeError):
        return jsonify({"message":"Enter all details to register"}), 400


@auth_v2.route('/login', methods=["POST"])
def login():
    try:
        data = request.get_json()
        errors = {}
        user = {}
        # check missing details
        if not data["username"] or not data["password"]:
            errors["missing_details"] = "Enter username and password to login"
        # check if user exists
        users = User.get_users(cur)
        for one_user in users:
            if one_user["username"] == data["username"]:
                user = one_user
        if not user:
            errors["missing_user"] = "User not found, register one first"
        if errors:
            return jsonify(errors), 401
        # check if given password matches username
        if check_password_hash(user["password"], data["password"]):
            token = jwt.encode({"username":user["username"], 
            "exp":datetime.datetime.utcnow() + datetime.timedelta(
                minutes=120)}, os.getenv('SECRET'))
            return jsonify({"token":token.decode("UTF-8")}), 200
        # check if authentication fails
        return jsonify({"authentication_error":"Username does not match password"}), 401
    except(ValueError, KeyError,TypeError):
        return jsonify({"message":"Enter all details to login"}), 400

@auth_v2.route("/users", methods=['GET'])
@auth_required
def get_users(current_user):
    """
    Return all users 
    """
    users = User.get_users(cur)
    if not users:
        return jsonify({"message": "No users found"}), 404
    return jsonify({"users": users}), 200
