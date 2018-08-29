import unittest
import json
from migration import migration
from app import create_app
from app.api.v2.models import User
from app.config import conn

from .views import valid_email_address, valid_username

cur = conn.cursor()

class CreateUserTestCase(unittest.TestCase):
    """
    This will contain test cases for a user
    """
    def setUp(self):
        """
        Will temporary hold data for testing users
        """
        migration()
        self.app = create_app(config_name="testing")
        self.client = self.app.test_client
        # set initial values to pass to the database
        self.test_user = {"username":"kavuku", "email":"kavuku@stack.com", "password":"pass123", "confirm_password":"pass123"}
        self.test_user1 = {"username":"kavuku1", "email":"kavuku1@stack.com", "password":"pass141", "confirm_password":"pass141"}
        self.test_login1 = {"username":"kavuku1", "password":"pass141"}
        self.another_user = {"username":"cinzia", "email":"cinzia@stack.com", "password":"mloi234", "confirm_password":"mloi234"}
        self.grande = {"username":"gianluca", "email":"gianluca@stack.com", "password":"0101", "confirm_password":"0101"}
        self.user = {"username":"michele", "email":"michele@stack.com", "password":"1040", "confirm_password":"4010"}
        self.user1 = {"username":"bravo", "email":"bravo@stack.com", "password":"3030", "confirm_password":"3030"}
        self.login_user = {"email":"mio@stack.com", "password":"1040"}

        self.token_user = {
            "username":"baba", 
            "email": "baba@stackoverflow.com",
            "password": "baba456",
            "confirm_password": "baba456"
        }
        self.login_token_user = {
            "username":"baba",
            "password": "baba456"
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
        print("<<<<<<<<<<<<<<<<<<,,")
        print(token_response.data)
        print("<<<<<<<<<<<<<<<<<<<<<<<<<")
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

    def test_valide_email(self):
        """
        Check the validity of an email address
        """
        correct_email = "tsofanyule@example.com"
        wrong_email = "tsofanyuleexample.com.com"
        self.assertTrue(valid_email_address(correct_email))
        self.assertFalse(valid_email_address(wrong_email))

    def test_valid_username(self):
        """
        Check the validity of username
        """
        correct_username = "tsofanyule"
        wrong_username = " "
        self.assertTrue(valid_username(correct_username))
        self.assertFalse(valid_username(wrong_username))

    def test_create_user(self):
        """
        Test if a user can be created
        """
        response = self.client().post('/api/v2/auth/register',
                                        data = json.dumps(self.test_user),
                                        content_type='application/json')
        self.assertEqual(response.status_code, 201)
        self.assertIn('User registered successfully', str(response.data))

    def test_user_can_login(self):
        """
        Test to check if an already registered user can log in
        """
        self.client().post('/api/v2/auth/register',
                                        data = json.dumps(self.test_user1),
                                        content_type='application/json')
        response = self.client().post('/api/v2/auth/login',
                                        data = json.dumps(self.test_login1),
                                        content_type='application/json')
        print("<<<<<<<<<<<<<<<<<")
        print(str(response.data))
        print("<<<<<<<<<<<<<<<<<")
        self.assertEqual(response.status_code, 200)

    def test_can_not_create_duplicate_user(self):
        """
        Test for twice user registration
        """
        self.client().post('/api/v2/auth/register',
                    data=json.dumps(self.another_user),
                    content_type='application/json')
        response = self.client().post('/api/v2/auth/register',
                    data=json.dumps(self.another_user),
                    content_type='application/json')
        self.assertIn("Username already exists", str(response.data))

    def test_some_details_missing(self):
        """
        Test api to ensure all required details are given before a user is created
        """
        response = self.client().post('/api/v2/auth/register',
                    data=json.dumps({
                        "username":"julius",
                        "password":"julius123",
                        "confirm_password":"julius123"
                    }),
                    content_type='application/json')
        self.assertIn("Enter all details to register", str(response.data))

    def test_get_all_users(self):
        """
        Test api if it can get all users
        """
        response = self.client().get('/api/v2/auth/users',
                    headers={'content-type':'application/json',
                        'x-access-token': self.token})
        self.assertEqual(response.status_code, 200)

    def test_empty_data(self):
        """
        Test api if can register user with empty data
        """
        response = self.client().post('/api/v2/auth/register',
                        data=json.dumps({
                            "username":"",
                            "email":"",
                            "password":"",
                            "confirm_password":""
                        }),
                        content_type='application/json')
        self.assertIn("Enter username, email, password and confirm_password", str(response.data))
        




