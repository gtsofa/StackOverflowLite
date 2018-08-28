# app/api/v2/questions/views.py
import os
import re
import jwt
import datetime

from flask import jsonify, request

from . import question_v2

from app.api.v2.models import Question
from app.api.v2.models import User
from app.api.v2.models import Answer
from app.api.v2.auth.views import auth_required 
from app.config import conn




cur = conn.cursor()
now = datetime.datetime.now()

def valid_question_title(title):
    if re.match(r'^(?=.*[A-Za-z])[a-zA-Z0-9\s\.,]{2,50}$', title):
        return True
    return False

def valid_description_text(description):
    if re.match(r'^(?=.*[A-Za-z])[^!@#\$%\^\*:]{2,300}$', description):
        return True

    return False



@question_v2.route('/questions', methods=["POST"])
@auth_required
def post_a_question(current_user):
    """
    Post a question
    """
    try:
        questions = Question.get_questions(cur)
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

@question_v2.route('/questions', methods=["GET"])
def get_all_questions():
    """
    Get all questions 
    """
    questions = Question.get_questions(cur)
    if not questions:
        return jsonify({"message": "No questions found"}), 404

    return jsonify({"questions": questions}), 200

@question_v2.route('/my-questions', methods=["GET"])
@auth_required
def get_all_users_questions(current_user):
    """
    Get all questions 
    """
    user_id = current_user["user_id"]
    questions = Question.get_users_questions(cur, user_id)
    if not questions:
        return jsonify({"message": "No questions found"}), 404

    return jsonify({"questions": questions}), 200


@question_v2.route('/questions/<int:questionID>', methods=["GET"])
def get_single_question(questionID):
    """
    Get a single question by id
    """
    question = Question.get_one_question(cur, questionID)
    if not question:
        return jsonify({"message": "Question not found"}), 404
    return jsonify(question)

@question_v2.route('/questions/<int:questionID>', methods=["DELETE"])
@auth_required
def delete_single_question(current_user, questionID):
    """
    Delete a single question by id
    """
    questions = Question.get_questions(cur)
    question = {}
    for one_question in questions:
        if one_question["question_id"] == questionID:
            question = one_question
    if not question:
        return jsonify({"missing_question": "Question not found"}), 404
    if question["user_id"] != current_user["user_id"]:
        return({"Unauthorised": "Users can only delete their questions"}), 401
    Question.delete_a_question(cur, questionID)
    return jsonify({"message": "Question deleted successfully"}), 200

@question_v2.route('/questions/<int:questionID>/answers', methods=["POST"])
@auth_required
def post_an_answer(current_user, questionID):
    """
    Post an answer to a question
    """
    try:
        data = request.get_json()
        errors = {}

        # check for missing details
        if not data['answer_text']:
            errors["missing_details"] = "Enter answer text"
        questions = Question.get_questions(cur)
        question = {}
        for one_question in questions:
            if one_question["question_id"] == questionID:
                question = one_question
        if not question:
            return jsonify({"missing_question": "Question not found"}), 404

        if errors:
            return jsonify(errors), 400

        user_id = current_user["user_id"]
        date_created = (now.strftime("%d-%m-%Y %H:%M:%S"))
        question_id = question["question_id"]
        preferred = False
        
        # everything is OK so save answer to db
        Answer.create_answer(cur , data["answer_text"], date_created, question_id, user_id, preferred)
        return jsonify({"message":"Answer successfully posted"}), 201
    except(ValueError, KeyError, TypeError):
        return jsonify({"message":"Enter all answer details to continue"}), 400

@question_v2.route('/questions/<int:questionID>/answers', methods=["GET"])
def get_all_answers_to_a_question(questionID):
    """
    Get all answers to a question 
    """
    errors = {}
    questions = Question.get_questions(cur)
    question = {}
    for one_question in questions:
        if one_question["question_id"] == questionID:
            question = one_question
    if not question:
        return jsonify({"missing_question": "Question not found"}), 404
    if errors:
        return jsonify(errors), 400
    answers = Answer.get_answers_to_question(cur, questionID)
    return jsonify({"answers": answers}), 200

# mark an answer as accepted or update an answer
@question_v2.route('questions/<int:questionID>/answers/<int:answerID>', methods=["PUT"])
@auth_required
def react_on_answer(current_user, questionID, answerID):
    """
    Mark answer as acepted or update an answer
    """
    data = request.get_json()
    errors = {}
    questions = Question.get_questions(cur)
    answers = Answer.get_answers_to_question(cur, questionID)
    question = {}
    answer = {}
    for one_question in questions:
        if one_question["question_id"] == questionID:
            question = one_question
    if not question:
        return jsonify({"missing_question": "Question not found"}), 404
    for one_answer in answers:
        if one_answer["answer_id"] == answerID:
            answer = one_answer
    if not answer:
        return jsonify({"missing_answer": "Answer not found"}), 404
    answer_id = answer["answer_id"]
    if errors:
        return jsonify(errors), 400
    Answer.modify_answer(cur, data["preferred"], answer_id)
    return jsonify({"message": "Answer marked as preferred successfully"}), 200

