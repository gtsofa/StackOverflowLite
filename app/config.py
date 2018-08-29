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
    conn = psycopg2.connect(
                "dbname=stack_test host=localhost user=stack password=stack123")

elif os.getenv('FLASK_CONFIG') == "development":

    conn = psycopg2.connect("postgres://wzlebjmkkdkbut:f01218aca2ecca508c9848f5759ee9094e1fa98b5d3e9ef22089a01d002d089b@ec2-54-235-86-226.compute-1.amazonaws.com:5432/d638bk9r7r4p2")

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