# app/api/v2/questions/test_questions

import unittest


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

    def tearDown(self):
        """
        Will destroy the test data after test runs
        """
        pass



    def test_user_can_post_a_question(self):
        """
        Test api if it can post a question
        """
        response = self.client().post('/api/v2/questions',
                    data=json.dumps(self.one_question),
                    content_type='application/json')
        self.assertEqual(response.status_code, 201)
        self.assertIn('Question posted successfully', str(response.data))
        
    def test_user_can_get_all_questions(self):
        """
        Test api can list all the questions
        """
        # Post a question
        self.client().post('/api/v2/questions',
                    data=json.dumps(self.one_question),
                    content_type='application/json')
        response = self.client().get('/api/v2/questions',
                    content_type='application/json')
        self.assertEqual(response.status_code,200)

    def test_user_can_view_one_question(self):
        """
        Test api can show one question
        """
        # Post a question
        self.client().post('/api/v2/questions',
                    data=json.dumps(self.one_question),
                    content_type='application/json')
        response = self.client().get('/api/v2/questions/1',
                    content_type='application/json')
        self.assertEqual(response.status_code,200)

    def test_user_cannot_view_missing_question(self):
        """
        Test api can show one question
        """
        # Post a question
        self.client().post('/api/v2/questions',
                    data=json.dumps(self.one_question),
                    content_type='application/json')
        response = self.client().get('/api/v2/questions/10',
                    content_type='application/json')
        self.assertIn('question does not exist', str(response.data))

    def test_user_can_get_users_questions(self):
        """
        Test api can list all the questions belonging to a user
        """
        # Post a question
        self.client().post('/api/v2/questions',
                    data=json.dumps(self.one_question),
                    content_type='application/json')
        response = self.client().get('/api/v2/my-questions',
                    content_type='application/json')
        self.assertEqual(response.status_code,200)

    def test_user_can_post_an_answer_to_question(self):
        """
        Test api if it can post an answer to a question
        """
        # Post a question
        self.client().post('/api/v2/questions',
                    data=json.dumps(self.one_question),
                    content_type='application/json')
        response = self.client().post('/api/v2/questions/1/answers',
                    data=json.dumps(self.one_answer),
                    content_type='application/json')
        self.assertEqual(response.status_code, 201)
        self.assertIn('Answer posted successfully', str(response.data))

    def test_user_can_get_answers_to_question(self):
        """
        Test api can list all the answers to a question
        """
        # Post a question
        self.client().post('/api/v2/questions',
                    data=json.dumps(self.one_question),
                    content_type='application/json')
        self.client().post('/api/v2/questions/1/answers',
                    data=json.dumps(self.one_answer),
                    content_type='application/json')
        response = self.client().get('/api/v2/my-questions',
                    content_type='application/json')
        self.assertEqual(response.status_code,200)