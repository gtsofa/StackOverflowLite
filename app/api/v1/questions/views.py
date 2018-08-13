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
all_questions = quizz.questions

@question.route('/questions', methods=['POST'])
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
    if len(all_users.keys()) == 0:
        errors["message"] = "No user exists. Register one first"
    if errors:
        return jsonify(errors), 400
    # Get the first user in the system
    first_user_key = list(all_users.keys())[0]
    first_user = all_users[first_user_key]
    user_id = first_user['user_id']
    question_id = len(all_questions) + 1
    date_posted = (now.day, now.month, now.year)
    # Create question if everything is OK
    new_question = {"question_id": question_id, "user_id":user_id, "question_title":data['question_title'], 
                "question_desc":data['question_desc'], "date_posted": date_posted}
    all_questions[question_id] = new_question
    return jsonify({"message" : "Question posted successfully", 
                                    "user_id": user_id}), 201

@question.route('/questions', methods=['GET'])
def get_questions():
    """
    Retrieve all questions in the system
    """
    return jsonify(all_questions), 200

@question.route('/my-questions', methods=['GET'])
@logged_in
def get_my_questions():
    """
    Retrieve all questions belonging to a user
    """
    errors = {}
    my_questions = []
    if len(all_users.keys()) == 0:
        errors["message"] = "No user exists. Register one first"
    if errors:
        return jsonify(errors), 400
    # Get the first user in the system
    first_user_key = list(all_users.keys())[0]
    first_user = all_users[first_user_key]
    user_id = first_user['user_id']
    for one_quizz in all_questions.values():
        if one_quizz.get("user_id") == user_id:
            my_questions.append(one_quizz)
    return jsonify({"my_questions": my_questions}), 200