# app/api/v2/questions/views.py
import os
import jwt
import datetime

from flask import jsonify, request

from . import question_v2

from app.api.v2.models import Question
from app.api.v2.models import User
from app.api.v2.models import Answer
from app.api.v2.auth.views import auth_required #token_valid
from config import conn


cur = conn.cursor()
now = datetime.datetime.now()


# post a question
@question_v2.route('/questions', methods=["POST"])
@auth_required
def post_a_question(current_user):
    """
    Post a question
    """
    try:
        questions = Question.get_questions(cur)
        # users = User.get_users(cur)
        data = request.get_json()
        errors = {}

        # check for missing details
        if not data['question_title'] or not data["question_desc"]:
            errors["missing_details"] = "Enter question title and question description"

        # check for duplicate question entry
        for question in questions:
            if question["question_title"] == data["question_title"]:

                errors["duplicate_question"] = "The question is already asked."

        if errors:
            return jsonify(errors), 400

        user_id = current_user["user_id"]
        date_created = (now.strftime("%d-%m-%Y %H:%M:%S"))

        # everything is OK so save question to db
        Question.create_question(cur , data["question_title"], data['question_desc'], date_created, user_id)
        return jsonify({"message":"Question successfully posted"}), 201
    except(ValueError, KeyError, TypeError):
        return jsonify({"message":"Enter all question details to continue"}), 400


# get all questions
@question_v2.route('/questions', methods=["GET"])
def get_all_questions():
    """
    Get all questions 
    """
    questions = Question.get_questions(cur)
    if not questions:
        return jsonify({"message": "No questions found"}), 404

    return jsonify({"questions": questions}), 200



# get a single question by id
@question_v2.route('/questions/<int:questionID>', methods=["GET"])
def get_single_question(questionID):
    """
    Get a single question by id
    """
    question = Question.get_one_question(cur, questionID)
    if not question:
        return jsonify({"message": "Question not found"}), 404
    return jsonify(question)
    

# mark an answer as acepted or update an answer
@question_v2.route('questions/questionID/answers/answerID', methods=["PUT"])
@auth_required
def react_on_answer():
    """
    Mark answer as acepted or update an answer
    """
    pass

