# config.py
import os
import psycopg2

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