# app/api/v2/models.py

from app.config import conn 
from flask import abort

class User:
    """
    Implement a user
    """
    def __init__(self, username, email, password, confirm_password):
        self.username = username
        self.email = email
        self.password = password
        self.confirm_password = confirm_password

    @staticmethod
    def create_user(cursor, username, email, password, confirm_password):
        query = "INSERT INTO users (username, email, password, confirm_password) VALUES (%s, %s, %s, %s);"
        cursor.execute(query, (username, email, password, confirm_password))
        conn.commit()

    @staticmethod
    def get_users(cursor):
        query = "SELECT * FROM users;"
        cursor.execute(query)
        users = cursor.fetchall()
        results = []
        for user in users:
            details = {}
            details["user_id"] = user[0]
            details["username"] = user[1]
            details["email"] = user[2]
            details["password"] = user[3]
            details["confirm_password"] = user[4]
            results.append(details)

        return results

    @staticmethod
    def get_single_user(cursor, user_id):
        query = "SELECT * FROM users WHERE user_id=%s;"
        cursor.execute(query, [user_id])
        user = cursor.fetchone()
        if not user:
            abort(404, "User not found")
        user_details = {}
        user_details["user_id"] = user[0]
        user_details["username"] = user[1]
        user_details["email"] = user[2]
        user_details["password"] = user[3]
        user_details["confirm_password"] = user[4]
        return user_details


class Question:
    """
    Implement a question
    """
    def __init__(self, question_title, question_desc, date_created, user_id):
        self.question_title = question_title
        self.question_desc = question_desc
        self.date_created = date_created
        self.user_id = user_id

    @staticmethod
    def create_question(cursor, question_title, question_desc, date_created, user_id):
        query = "INSERT INTO questions (title, description, date_created, user_id) VALUES (%s, %s, %s, %s);"
        cursor.execute(query, (question_title, question_desc, date_created, user_id))
        conn.commit()

    @staticmethod
    def get_questions(cursor):
        query = "SELECT * FROM questions ORDER by date_created DESC;"
        cursor.execute(query)
        questions = cursor.fetchall()
        response = []
        for question in questions:
            details_data = {}
            details_data["question_id"] = question[0]
            details_data["question_title"] = question[1]
            details_data["question_desc"] = question[2]
            details_data["date_created"] = question[3]
            details_data["user_id"] = question[4]
            response.append(details_data)
        return response

    @staticmethod
    def get_users_questions(cursor, user_id):
        query = "SELECT * FROM questions WHERE user_id=%s;"
        cursor.execute(query, [user_id])
        questions = cursor.fetchall()
        response = []
        for question in questions:
            details_data = {}
            details_data["question_id"] = question[0]
            details_data["question_title"] = question[1]
            details_data["question_desc"] = question[2]
            details_data["date_created"] = question[3]
            details_data["user_id"] = question[4]
            response.append(details_data)

        return response

    @staticmethod
    def get_one_question(cursor, question_id):
        query = "SELECT * FROM questions WHERE id=%s;"
        cursor.execute(query, [question_id])
        question = cursor.fetchone()
        if not question:
            abort(404, "Question not found")
        details_data = {}
        details_data["question_id"] = question[0]
        details_data["question_title"] = question[1]
        details_data["question_desc"] = question[2]
        details_data["date_created"] = question[3]
        details_data["user_id"] = question[4]
        return details_data

    @staticmethod
    def edit_single_question(cursor, question_title, question_desc, date_created, user_id):
        query = "UPDATE questions SET question_title=%s, question_desc=%s, date_created=%s, user_id=%s;"
        cursor.execute(query, (question_title, question_desc, date_created, user_id))
        conn.commit()

    @staticmethod
    def delete_a_question(cursor, question_id):
        query = "DELETE FROM questions WHERE id=%s;"
        cursor.execute(query, [question_id])

class Answer:
    """
    Implement the answer
    """
    def __init__(self, answer_text):
        self.answer_text = answer_text

    @staticmethod
    def create_answer(cursor, answer_text, date_created, question_id, user_id, preferred):
        query = "INSERT INTO answers(answer_text, date_created, question_id, user_id, preferred) VALUES (%s, %s, %s, %s, %s);"
        cursor.execute(query, (answer_text, date_created, question_id, user_id, preferred))
        conn.commit()

    @staticmethod
    def get_answers_to_question(cursor, question_id):
        query = "SELECT * FROM answers WHERE question_id=%s;"
        cursor.execute(query, [question_id])
        answers = cursor.fetchall()
        response = []
        for answer in answers:
            details_data = {}
            details_data["answer_id"] = answer[0]
            details_data["answer_text"] = answer[1]
            details_data["date_created"] = answer[2]
            details_data["question_id"] = answer[3]
            details_data["user_id"] = answer[4]
            details_data["preferred"] = answer[5]
            response.append(details_data)

        return response

    @staticmethod
    def modify_answer(cursor, preferred, answer_id):
        query = "UPDATE answers SET preferred=%s WHERE (id=%s)"
        cursor.execute(query, (preferred, answer_id))
        conn.commit()




        


