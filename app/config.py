# config.py
import os
import psycopg2

# try:
#     conn_test = psycopg2.connect(
#         "dbname=stack_test host=localhost user=stack password=stack123")
# except Exception as e:
#     print("Unable to connect to the database", e)
# try:
#     conn = psycopg2.connect(
#         "dbname=stack_dev host=localhost user=stack password=stack123")
# except Exception as e:
#     print("Unable to connect to the database", e)

if os.getenv('FLASK_CONFIG') == "testing":
    conn = psycopg2.connect(os.getenv('DATABASE_TEST_URL'))

elif os.getenv('FLASK_CONFIG') == "development":

    conn = psycopg2.connect(os.getenv('DATABASE_URL'))

else:
    print("Unable to connect to the database")
    

class Config(object):
    """Default configuration"""

    DEBUG = False
    TESTING = False
    SECRET = os.getenv("SECRET")

class TestingConfig(Config):
    """Testing configuration"""
    DEBUG = True
    TESTING = True

class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    TESTING = True

class ProductionConfig(Config):
    """Development configuration"""
    DEBUG = False
    TESTING = False

app_config = {
    "development" : DevelopmentConfig,
    "production" : ProductionConfig,
    "testing" : TestingConfig
}