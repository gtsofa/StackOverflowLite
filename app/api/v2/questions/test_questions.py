# app/api/v2/questions/test_questions

import unittest
import json
from app import create_app
from app.config import conn

from .views import valid_question_title, valid_description_text

cur = conn.cursor()

class CreateQuestionTestCase(unittest.TestCase):
    """
    Contains the test cases for questions
    """
    def setUp(self):
        """
        Will hold data for test purposes 
        """
        self.app = create_app(config_name="testing")
        self.client = self.app.test_client

        self.user = {
            "username":"mama", 
            "email": "leeann@stackoverflow.com",
            "password": "Mama456",
            "confirm_password": "Mama456"
        }
        self.token_user = {
            "username":"baba", 
            "email": "baba@stackoverflow.com",
            "password": "baba456",
            "confirm_password": "baba456"
        }
        self.login_user = {
            "username":"mama",
            "password": "Mama456"
        }
        self.login_token_user = {
            "username":"baba",
            "password": "baba456"
        }
        self.one_question = {
            "question_title":"What is Flask",
            "question_desc":"I am a beginner and I wanna know what flask is"
        } 

        self.one_question1 = {
            "question_title":"What is Flask",
            "question_desc":"I am a beginner and I wanna know what flask is",
            "preferred":True
        } 
        self.two_question = {
            "question_title":"What is Postgres",
            "question_desc":"Lorem ipsum dolor sit amet"
        }
        self.three_question = {
            "question_title":"Who is the queen of vionilist?",
            "question_desc":"I guess MeriBenari takes the show by far if the research says so psum dolor sit amet"
        }
        self.one_answer = {
            "answer_text":"Flask is a Python microframework"
        }
        self.reg_user = {
            "username":"john", 
            "email": "john@stackoverflow.com",
            "password": "Mama456",
            "confirm_password": "Mama456"
        }
        self.login_reg_user = {
           "username":"john",
            "password": "Mama456"
        }
        # Register a user
        self.client().post('/api/v2/auth/register', 
                    data=json.dumps(self.token_user),
                    content_type='application/json')
        # Sign in user
        token_response = self.client().post('/api/v2/auth/login',
                    data=json.dumps(self.login_token_user),
                    content_type='application/json')
        data = json.loads(token_response.data.decode())
        self.token = data['token']
        

    def tearDown(self):
        """
        Will destroy the test data after test runs
        """
        answers_query = "DELETE FROM answers;"
        questions_query = "DELETE FROM questions;"
        users_query = "DELETE FROM users;"
        reset_users = "ALTER SEQUENCE users_id_seq RESTART WITH 1;"
        reset_questions = "ALTER SEQUENCE questions_id_seq RESTART WITH 1;"
        reset_answers = "ALTER SEQUENCE answers_id_seq RESTART WITH 1;"
        cur.execute(reset_answers)
        cur.execute(reset_questions)
        cur.execute(reset_users)
        cur.execute(answers_query)
        cur.execute(questions_query)
        cur.execute(users_query)
        conn.commit()


        

    def test_valid_question_title(self):
        """
        Test valid questions titles are allowed
        """
        correct_title = "How do nasa travel to saturn"
        wrong_title = ' '
        self.assertTrue(valid_question_title(correct_title))
        self.assertFalse(valid_question_title(wrong_title))
        
    def test_user_can_post_a_question(self):
        """
        Test if a user can post a question
        """
        response = self.client().post('/api/v2/questions',
                    data=json.dumps(self.one_question),
                    headers={'content-type':'application/json',
                        'x-access-token': self.token})
        self.assertEqual(response.status_code, 201)
        self.assertIn('Question successfully posted', str(response.data))
        
    def test_user_can_get_all_questions(self):
        """
        Test if a user can fetch a list of all questions
        """
        # Post a question
        self.client().post('/api/v2/questions',
                    data=json.dumps(self.one_question),
                    headers={'content-type':'application/json',
                        'x-access-token': self.token})
        response = self.client().get('/api/v2/questions',
                    content_type='application/json')
        self.assertEqual(response.status_code,200)

    def test_user_can_get_a_single_question(self):
        """
        Test if a user can fetch a single question by questionID
        """
        # Post a question
        self.client().post('/api/v2/questions',
                    data=json.dumps(self.one_question),
                    headers={'content-type':'application/json',
                        'x-access-token': self.token})
        response = self.client().get('/api/v2/questions/1',
                    content_type='application/json')
        self.assertEqual(response.status_code,200)

    def test_get_a_question_that_doesnt_exits(self):
        """
        Test if a user can get a question that doesn't exists
        """
        # Post a question
        self.client().post('/api/v2/questions',
                    data=json.dumps(self.one_question),
                    content_type='application/json')
        response = self.client().get('/api/v2/questions/10',
                    content_type='application/json')
        self.assertIn('Question not found', str(response.data))

    def test_user_can_fetch_their_own_questions(self):
        """
        Test if a user can get a list of all their questions on the app
        """
        # Post a question
        self.client().post('/api/v2/questions',
                    data=json.dumps(self.one_question),
                    headers={'content-type':'application/json',
                        'x-access-token': self.token})
        response = self.client().get('/api/v2/my-questions',
                    headers={'content-type':'application/json',
                        'x-access-token': self.token})
        self.assertEqual(response.status_code,200)

    def test_user_can_answer_a_question(self):
        """
        Test if a user can post answer to a question
        """
        # Post a question
        r = self.client().post('/api/v2/questions',
                    data=json.dumps(self.one_question),
                    headers={'content-type':'application/json',
                        'x-access-token': self.token})
        response1 = self.client().post('/api/v2/questions/1/answers',
                    data=json.dumps(self.one_answer),
                    headers={'content-type':'application/json',
                        'x-access-token': self.token})
        self.assertEqual(response1.status_code, 201)
        self.assertEqual('Answer successfully posted', response1.json['message'])

    def test_user_can_get_answers_to_question(self):
        """
        Test if a user can get a list of all the answers to a question
        """
        # Post a question
        self.client().post('/api/v2/questions',
                    data=json.dumps(self.one_question),
                    headers={'content-type':'application/json',
                        'x-access-token': self.token})
        self.client().post('/api/v2/questions/1/answers',
                    data=json.dumps(self.one_answer),
                    headers={'content-type':'application/json',
                        'x-access-token': self.token})
        response = self.client().get('/api/v2/questions/1/answers',
                    content_type='application/json')
        self.assertEqual(response.status_code,200)
    
    def test_user_can_delete_own_question(self):
        """
        Test if a user can delete their own question
        """
        # delete api/v2/questions/my-questions/1
        # post a question
        self.client().post('/api/v2/questions/1',
                        data=json.dumps(self.three_question),
                        headers={'content-type':'application/json',
                        'x-access-token': self.token})

    def test_user_can_mark_an_answer_as_accepted_or_update_an_answer(self):
        """
        Test if a question author can accept answer or answer author can update their answer
        """
        r1 = self.client().post('/api/v2/questions',
                    data=json.dumps(self.one_question),
                    headers={'content-type':'application/json',
                        'x-access-token': self.token})
        r2 = self.client().post('/api/v2/questions/1/answers',
                    data=json.dumps(self.one_answer),
                    headers={'content-type':'application/json',
                        'x-access-token': self.token})
        response = self.client().put('/api/v2/questions/1/answers/1',
                    data=json.dumps(self.one_question1, ),
                    headers={'content-type':'application/json',
                        'x-access-token': self.token})
        self.assertEqual(response.status_code,200)
