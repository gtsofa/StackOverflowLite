import unittest
import json
from migration import migration
from app import create_app
from app.api.v2.models import User


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
        self.test_login = {"email":"mae@stack.com", "password":"pass141"}
        self.another_user = {"username":"cinzia", "email":"cinzia@stack.com", "password":"mloi234", "confirm_password":"mloi234"}
        self.grande = {"username":"gianluca", "email":"gianluca@stack.com", "password":"0101", "confirm_password":"0101"}
        self.user = {"username":"michele", "email":"michele@stack.com", "password":"1040", "confirm_password":"4010"}
        self.user1 = {"username":"bravo", "email":"bravo@stack.com", "password":"3030", "confirm_password":"3030"}
        self.login_user = {"email":"mio@stack.com", "password":"1040"}

    def tearDown(self):
        """
        destroy the test data for testing purposes
        """
        self.test_user.clear()
        self.test_login.clear()
        self.another_user.clear()
        self.grande.clear()
        self.user.clear()
        self.login_user.clear()

    def test_create_user(self):
        """
        Test if a user can be created
        """
        response = self.client().post('/app/api/v2/auth/register',
                                        data = json.dumps(self.test_user),
                                        content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertIn('User registered successfully', str(response.data))

    def test_user_can_login(self):
        """
        Test to check if an already registered user can log in
        """
        response = self.client().post('/app/api/v2/auth/login',
                                        data = json.dumps(self.test_login),
                                        content_type='application/json')
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
        self.client().post('/api/v2/auth/register', 
                    data=json.dumps(self.test_user),
                    content_type='application/json')
        self.client().post('/api/v2/auth/login',
                    data=json.dumps(self.grande),
                    content_type='application/json')
        response = self.client().get('/api/v2/auth/users',
                    content_type='application/json')
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
        self.assertIn("Enter username, email, password, and confirm password to register", str(response.data))
        




