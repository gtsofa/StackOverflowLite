from flask import jsonify

from . import auth
from app.api.v1.auth.models import User

@auth.route('/register', methods=['GET'])
def register_user():
    """Register a new user"""
    return jsonify({"message": "Good"})