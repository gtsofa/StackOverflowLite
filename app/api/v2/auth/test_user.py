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
        self.test_user = {"username":"maestro", "email":"maestro@stack.com", "password":"pass123"}
        self.test_login = {"email":"tsofa@stack.com", "password":"pass141"}

        



