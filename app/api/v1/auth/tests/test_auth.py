import unittest
import json
from app import create_app

class CreateUserTestCase(unittest.TestCase):
    """
    This class tests the User 
    """
    def setUp(self):
        """
        This method will be called before every time a test runs, 
        and will create data for use by the tests
        """
        self.app = create_app(config_name="testing")
        create_app.testing = True
        self.client = self.app.test_client

        self.user = {
            "username":"maestro",
            "email":"maestro@stackoverflow.com",
            "password":"amka123",
            "confirm_password":"amka123"
        }
        self.login_user = {
            "username":"maestro",
            "password":"amka123"
        }
        self.register_user = {
            "username":"tsofa",
            "email":"tsofa@stackoverflow.com",
            "password":"amka123",
            "confirm_password":"amka123"
        }

    def tearDown(self):
        """
        This method will be called after the tests run. 
        It will help to clear data after every test
        """
        self.user.clear()
        self.login_user.clear()
        self.register_user.clear()

    def test_sign_up_user(self):
        """
        Test api if it can register a new user
        """
        response = self.client().post('/api/v1/auth/register', 
                    data=json.dumps(self.register_user),
                    content_type='application/json')
        self.assertEqual(response.status_code, 201)
        self.assertIn('User registered successfully', str(response.data))

    def test_can_not_create_duplicate_user(self):
        """
        Test api can only allow one user creation
        """
        self.client().post('/api/v1/auth/register',
                    data=json.dumps(self.user),
                    content_type='application/json')
        response = self.client().post('/api/v1/auth/register',
                    data=json.dumps(self.user),
                    content_type='application/json')
        self.assertIn("Username already exists", str(response.data))

    def test_blank_data(self):
        """
        Test api to ensure no details are ommited 
        """
        response = self.client().post('/api/v1/auth/register',
                    data=json.dumps({
                        "username":"",
                        "email":"",
                        "password":"",
                        "confirm_password":""
                    }),
                    content_type='application/json')
        self.assertIn("Enter username, email, password and confirm password to register", str(response.data))

    def test_some_details_missing(self):
        """
        Test api to ensure all expected values are given 
        """
        response = self.client().post('/api/v1/auth/register',
                    data=json.dumps({
                        "username":"julius",
                        "password":"julius123",
                        "confirm_password":"julius123"
                    }),
                    content_type='application/json')
        self.assertIn("Enter all details to register", str(response.data))
        
    def test_sign_in_user(self):
        """
        Test api if it can sign in existing user
        """
        self.client().post('/api/v1/auth/register', 
                    data=json.dumps(self.user),
                    content_type='application/json')
        response = self.client().post('/api/v1/auth/login',
                    data=json.dumps(self.login_user),
                    content_type='application/json')
                    
        self.assertEqual(response.status_code, 200)
        self.assertIn("logged in successfully", str(response.data))
        
    def test_get_all_users(self):
        """
        Test api if it can get all users
        """
        self.client().post('/api/v1/auth/register', 
                    data=json.dumps(self.user),
                    content_type='application/json')
        self.client().post('/api/v1/auth/login',
                    data=json.dumps(self.login_user),
                    content_type='application/json')
        response = self.client().get('/api/v1/auth/users',
                    content_type='application/json')
        self.assertEqual(response.status_code, 200)

    def test_sign_out_user(self):
        """
        Test api can sign out a user
        """
        # Register user
        self.client().post('/api/v1/auth/register', 
                    data=json.dumps(self.user),
                    content_type='application/json')
        # Sign in user
        self.client().post('/api/v1/auth/login',
                    data=json.dumps(self.login_user),
                    content_type='application/json')
        # Log user out
        response = self.client().post('/api/v1/auth/logout',
                    data=json.dumps(self.user),
                    content_type='application/json')
        self.assertEqual(response.status_code, 200)
