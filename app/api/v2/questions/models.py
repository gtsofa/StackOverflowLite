
# from config import conn

# class Question:
#     """
#     Implement a question
#     """
#     def __init__(self, question_title, question_desc):
#         self.question_title = question_title
#         self.question_desc = question_desc

#     @staticmethod
#     def create_question(cursor, question_title, question_desc):
#         query = "INSERT INTO questions (question_title, question_desc) VALUES (%s, %s);"
#         cursor.execute(query, (question_title, question_desc))
#         conn.commit()

#     @staticmethod
#     def get_questions(cursor):
#         query = "SELECT * FROM questions;"
#         cursor.execute(query)
#         questions = cursor.execute.fetchall()
#         response = []
#         for question in questions:
#             details_data = {}
#             details_data["question_id"] = question[0]
#             details_data["question_title"] = question[1]
#             details_data["question_desc"] = question[2]
#             details_data["user_id"] = question[3]
#             details_data["date_modified"] = question[4]
#             response.append(details_data)

#         return response


# class Answer:
#     """
#     Implement the answer
#     """
#     def __init__(self, answer_body):
#         self.answer_body = answer_body

#     @staticmethod
#     def create_answer(cursor, answer_body):
#         query = "INSERT INTO answers(answer_body) VALUES (%s);"
#         cursor.execute(query, (answer_body))
#         conn.commit()

#     @staticmethod
#     def get_answers(cursor):

#         # how to fetch answers belong to a question
#         pass