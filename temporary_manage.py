# migration.py

# create a tables for the application

import os
from config import app_config
from app import create_app

config_name = os.getenv('FLASK_CONFIG')
app = create_app(config_name)
conn = app.config["CONN"]

def migration():
    """
    create tables on the database
    """
    cur = conn.cursor()

    try:
        # delete tables if they exist
        cur.execute("DROP TABLE IF EXISTS users, questions, answers, comments;")

        # create user table
        users = """CREATE TABLE users(
            id SERIAL PRIMARY KEY,
            username VARCHAR(50),
            email VARCHAR(50) UNIQUE,
            password VARCHAR(250),
            confirm_password VARCHAR(250)

        );"""

        # create questions table
        questions = """CREATE TABLE questions (
            id SERIAL PRIMARY KEY,
            title VARCHAR(50),
            description TEXT,
            date_created TIMESTAMP,
            user_id INT references users(id)
        );"""

        # create answers table
        answers = """CREATE TABLE answers (
            id SERIAL PRIMARY KEY,
            answer_text TEXT,
            date_created TIMESTAMP,
            question_id INT references questions(id),
            user_id INT references users(id)
        );"""

        # create comments table
        comments = """CREATE TABLE comments (
            id SERIAL PRIMARY KEY,
            comments_text TEXT,
            date_created TIMESTAMP,
            question_id INT references questions(id),
            user_id INT references users(id),
            answer_id INT references answers(id)
        );"""

        cur.execute(users)
        cur.execute(questions)
        cur.execute(answers)
        cur.execute(comments)

        conn.commit()

    except Exception as e:
        print("Error", e)

migration()