from flask import Blueprint
auth_v2 = Blueprint('auth_v2', __name__)
from . import views