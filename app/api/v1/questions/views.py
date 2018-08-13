import datetime
from flask import jsonify, request

from . import question
from app.api.v1.questions.models import Question, Answer
from app.api.v1.auth.models import User
from app.api.v1.questions.models import Answer
from app.api.v1.auth.views import logged_in, all_users

quizz = Question()
ans = Answer()
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

@question.route('/questions/<int:question_id>', methods=['GET'])
def get_one_questions(question_id):
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
        data = request.get_json()
        answer_id = len(ans.answers) + 1
        question_id = single_question["question_id"]
        # Get user id
        if len(all_users.keys()) == 0:
            errors["message"] = "No user exists. Register one first"
        if errors:
            return jsonify(errors), 400
        # Get the first user in the system
        first_user_key = list(all_users.keys())[0]
        first_user = all_users[first_user_key]
        user_id = first_user['user_id']
        date_posted = (now.day, now.month, now.year)
        new_answer = {"answer_id": answer_id, "question_id": question_id, 
                        "answer_text": data["answer_text"], "date_posted": date_posted,
                        "user_id": user_id}
        ans.answers[answer_id] = new_answer
        return jsonify({"message": "Answer posted successfully"}), 200

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