from app import create_app
import unittest
import json

class QuestionTestCase(unittest.TestCase):
    """
    Test class for testing questions and answers 
    """
    def setUp(self):
        
        """
        Method hold data for tests before the tests run
        """
        self.app = create_app(config_name="testing")
        self.client = self.app.test_client
        self.one_question = {
            "question_title":"What is Flask",
            "question_desc":"I am a beginner and I wanna know what flask is"
        } 
        self.two_question = {
            "question_title":"What is Postgres",
            "question_desc":"Lorem ipsum dolor sit amet"
        }
        self.one_answer = {
            "answer_text":"Flask is a Python microframework"
        }
        
    def tearDown(self):
        """
        This method will be called after the tests run. 
        It will help to clear data after every test
        """
        self.one_question.clear()
        self.two_question.clear()

    def test_user_can_post_a_question(self):
        """
        Test api if it can post a question
        """
        response = self.client().post('/api/v1/questions',
                    data=json.dumps(self.one_question),
                    content_type='application/json')
        self.assertEqual(response.status_code, 201)
        self.assertIn('Question posted successfully', str(response.data))
        
    def test_user_can_get_all_questions(self):
        """
        Test api can list all the questions
        """
        # Post a question
        self.client().post('/api/v1/questions',
                    data=json.dumps(self.one_question),
                    content_type='application/json')
        response = self.client().get('/api/v1/questions',
                    content_type='application/json')
        self.assertEqual(response.status_code,200)

    def test_user_can_view_one_question(self):
        """
        Test api can show one question
        """
        # Post a question
        self.client().post('/api/v1/questions',
                    data=json.dumps(self.one_question),
                    content_type='application/json')
        response = self.client().get('/api/v1/questions/1',
                    content_type='application/json')
        self.assertEqual(response.status_code,200)

    def test_user_cannot_view_missing_question(self):
        """
        Test api can show one question
        """
        # Post a question
        self.client().post('/api/v1/questions',
                    data=json.dumps(self.one_question),
                    content_type='application/json')
        response = self.client().get('/api/v1/questions/10',
                    content_type='application/json')
        self.assertIn('question does not exist', str(response.data))


    def test_user_can_post_an_answer_to_question(self):
        """
        Test api if it can post an answer to a question
        """
        # Post a question
        self.client().post('/api/v1/questions',
                    data=json.dumps(self.one_question),
                    content_type='application/json')
        response = self.client().post('/api/v1/questions/1/answers',
                    data=json.dumps(self.one_answer),
                    content_type='application/json')
        self.assertEqual(response.status_code, 201)
        self.assertIn('Answer posted successfully', str(response.data))

    def test_user_can_get_answers_to_question(self):
        """
        Test api can list all the answers to a question
        """
        # Post a question
        self.client().post('/api/v1/questions',
                    data=json.dumps(self.one_question),
                    content_type='application/json')
        self.client().post('/api/v1/questions/1/answers',
                    data=json.dumps(self.one_answer),
                    content_type='application/json')
        response = self.client().get('/api/v1/questions/1/answers',
                    content_type='application/json')
        self.assertEqual(response.status_code,200)