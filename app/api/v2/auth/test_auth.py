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
        pass

    def tearDown(self):
        """
        This method will be called after the tests run. 
        It will help to clear data after every test
        """
        pass

    def test_sign_up_user(self):
        """
        Test api if it can register a new user
        """
        pass

    def test_can_not_create_duplicate_user(self):
        """
        Test api can only allow one user creation
        """
        pass

    def test_blank_data(self):
        """
        Test api to ensure no details are ommited 
        """
        pass

    def test_some_details_missing(self):
        """
        Test api to ensure all expected values are given 
        """
        pass
        
    def test_sign_in_user(self):
        """
        Test api if it can sign in existing user
        """
        pass
    def test_get_all_users(self):
        """
        Test api if it can get all users
        """
        pass

    def test_sign_out_user(self):
        """
        Test api can sign out a user
        """
        # Register user
        pass
        # Sign in user
        pass
        # Log user out
        pass