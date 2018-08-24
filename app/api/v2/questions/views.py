# app/api/v2/questions/views.py
import datetime

from flask import jsonify, request

from . import question_v2

from app.api.v2.questions.models import Question, Answer
from app.api.v2.auth.models import User
from app.api.v2.questions.models import Answer
from app.api.v2.auth.views import token_required, token_valid


cur = conn.cursor()
users = User.get_users(cur)
questions = Question.get_questions(cur)


# post a question
@question_v2.route('/questions', methods=["POST"])
@token_required
@token_valid
def post_a_question(current_user):
    """
    Post a question
    """
    try:

        data = request.get_json()
        errors = {}
        user = current_user
        questions = questions.query_all()

        # check for details
        if not data['question_title'] or not data["question_desc"]:
            errors["missing_details"] = "Enter question title and question description"

        # check for duplicate question entry
        for question in questions:
            if question["question_title"] == data["question_title"]:
                return errors["duplicate_question"] = "The question is already asked."

        if errors:
            return jsonify(errors), 400

        user_id = current_user.id
        question_id = len(all_questions) + 1
        date_posted = (now.day, now.month, now.year)

        # everything is OK so save question to db
        Question.create_question(cur , question_id, data["question_title"], user_id, data['question_desc'], date_posted)
        return jsonify({"message":"Question successfully posted"}), 201
    except(ValueError, KeyError, TypeError)
        return jsonify({"message":"Enter all question details to continue"}), 400


# get all questions
@question_v2.route('/questions', methods=["GET"])
@token_required
def get_all_questions(current_user):
    """
    Get all questions for a user
    """
    questions = Question.query.filter_by(user_id=current_user.id)

    results = []
    for question in questions:
        question_data = {}
        question_data['question_title'] = question.title
        question_data["question_desc"] = question.description
        results.append(question_data)
        
    return jsonify({"question": results}), 200



# get a single question by id
@question_v2.route('/questions/questionID', methods=["GET"])
def get_single_question(questionID):
    """
    Get a single question by id
    """
    

# mark an answer as acepted or update an answer
@question_v2.route('questions/questionID/answers/answerID', methods=["PUT"])
@token_required
@token_valid
def edit_answer():
    """
    Mark answer as acepted or update an answer
    """
    pass

