import datetime
from flask import jsonify, request

from . import question
from app.api.v1.questions.models import Question
from app.api.v1.auth.models import User
from app.api.v1.questions.models import Answer
from app.api.v1.auth.views import logged_in, all_users

quizz = Question()
user = User()
now = datetime.datetime.now()

@question.route('', methods=['POST'])
@logged_in
def post_question():
    """
    Post a question
    """
    errors = {}
    data = request.get_json()
    # Check for details
    if not data['question_title'] or not data['question_desc']:
        errors['missing_details'] = "Enter username, email, password and confirm password to register"
    if errors:
        return jsonify(errors), 400
    # Get the first user in the system
    if len(all_users.keys()) == 0:
        return jsonify({"message": "No user exists. Register one first"})
    first_user_key = list(all_users.keys())[0]
    first_user = all_users[first_user_key]
    user_id = first_user['user_id']
    question_id = len(quizz.questions) + 1
    date_posted = (now.day, now.month, now.year)
    # Create question if everything is OK
    new_question = {"question_id": question_id, "user_id":user_id, "question_title":data['question_title'], 
                "question_desc":data['question_desc'], "date_posted": date_posted}
    quizz.questions[question_id] = new_question
    return jsonify({"message" : "Question posted successfully", 
                                    "user_id": user_id}), 201

