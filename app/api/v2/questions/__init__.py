from flask import Blueprint

question_v2 = Blueprint('question_v2', __name__)

from . import views
