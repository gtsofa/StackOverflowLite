import datetime
from flask import jsonify, request

from . import question
from app.api.v1.questions.models import Question, Answer
from app.api.v1.questions.models import Answer

quizz = Question()
ans = Answer()
now = datetime.datetime.now()
all_questions = quizz.questions

@question.route('/questions', methods=['POST'])
def post_question():
    """
    Post a question
    """
    try:
        errors = {}
        data = request.get_json()
        # Check for details
        if not data['question_title'] or not data['question_desc']:
            errors['missing_details'] = "Enter a question title and description to post a question"
        if errors:
            return jsonify(errors), 400
        question_id = len(all_questions) + 1
        date_posted = (now.day, now.month, now.year)
        # Create question if everything is OK
        new_question = {"question_id": question_id, "question_title":data['question_title'], 
                    "question_desc":data['question_desc'], "date_posted": date_posted}
        all_questions[question_id] = new_question
        return jsonify({"message" : "Question posted successfully"}), 201
    except (ValueError, KeyError, TypeError):
        return jsonify({"message": "Enter all details to post a question"}), 400

@question.route('/questions', methods=['GET'])
def get_questions():
    """
    Retrieve all questions in the system
    """
    return jsonify(all_questions), 200

@question.route('/questions/<int:question_id>', methods=['GET'])
def get_one_question(question_id):
    """
    Retrieve a single question from the system
    """
    errors = {}
    single_question = {}
    error = []
    if len(all_questions) == 0:
        errors['message'] = "There are no questions. Post one first"
    for one_question in quizz.questions.values():
        if one_question["question_id"] == question_id:
            single_question = one_question
        else:
            error.append("The question does not exist.")
    if len(single_question) == 0:
        errors["missing_question"] = "The question does not exist."
    if errors:
        return jsonify(errors)
    return jsonify(single_question), 200

@question.route('/questions/<int:question_id>/answers', methods=['POST', 'GET'])
def post_answer_to_question(question_id):
    """
    Post an answer to a question and retrieve the answer
    """
    # Get one question
    errors = {}
    single_question = {}
    error = []
    if len(all_questions) == 0:
        errors['message'] = "There are no questions. Post one first"
    for one_question in quizz.questions.values():
        if one_question["question_id"] == question_id:
            single_question = one_question
        else:
            error.append("The question does not exist.")
    if len(single_question) == 0:
        errors["missing_question"] = "The question does not exist."
    if errors:
        return jsonify(errors), 400
    
    # Post an answer to a question
    if request.method == 'POST':
        try:
            data = request.get_json()
            answer_id = len(ans.answers) + 1
            question_id = single_question["question_id"]
            if errors:
                return jsonify(errors), 400
            date_posted = (now.day, now.month, now.year)
            new_answer = {"answer_id": answer_id, "question_id": question_id, 
                            "answer_text": data["answer_text"], "date_posted": date_posted}
            ans.answers[answer_id] = new_answer
            return jsonify({"message": "Answer posted successfully"}), 201
        except (ValueError, KeyError, TypeError):
            return jsonify({"message": "Enter all details to post an answer"}), 400

    # Get all answers for a question
    if request.method == 'GET':
        question_answers = []
        error = []
        question_id = single_question["question_id"]
        for one_answer in ans.answers.values():
            if one_answer["question_id"] == question_id:
                question_answers.append(one_answer)
            else:
                error.append("There are no answers to this question")
        if len(one_answer) == 0:
            errors["missing_question"] = error[0]
        if errors:
            return jsonify(errors)
        return jsonify({"answers": question_answers})