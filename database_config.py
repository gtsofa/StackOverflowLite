# config.py
import os
import psycopg2

if os.getenv('FLASK_CONFIG') == 'testing':
    DATABASE_URI = "dbname=stack_test host=localhost user=stack password=stack123"
DATABASE_URI = "dbname=stack_dev host=localhost user=stack password=stack123"

try:
    conn = psycopg2.connect(DATABASE_URI)
except Exception as e:
    print("Unable to connect to the database", e)

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