import os
import psycopg2
from app import create_app

config_name = os.getenv('FLASK_CONFIG')
app = create_app(config_name)

db_uri = app.config["DB_URI"]

try:
    conn = psycopg2.connect(db_uri)
except Exception as e:
    print("Unable to connect to the database", e)
