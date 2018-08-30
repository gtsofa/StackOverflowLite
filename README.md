# StackOverflowLite
[![Build Status](https://travis-ci.org/gtsofa/StackOverflowLite.svg?branch=develop)](https://travis-ci.org/gtsofa/StackOverflowLite)
[![Coverage Status](https://coveralls.io/repos/github/gtsofa/StackOverflowLite/badge.svg?branch=develop)](https://coveralls.io/github/gtsofa/StackOverflowLite?branch=develop)
[![Maintainability](https://api.codeclimate.com/v1/badges/e24f0a3fc8795071da2e/maintainability)](https://codeclimate.com/github/gtsofa/StackOverflowLite/maintainability)

#### Project Overview
StackOverflowLite is a platform where people can ask questions and provide answers.

#### Required Features
1. A user can create an account and log in
2. A user can post questions
3. A user can delete the questions they post
4. A user can post answers
5. A user can view the answers to the questions
6. A user can accept answer out of all answers to his/her questions as the preferred answer.

## Challenge 1 - Create UI Templates

#### The Interface
1. [Home Page](https://gtsofa.github.io/StackOverflowLite/UI/)
2. [User Registration](https://gtsofa.github.io/StackOverflowLite/UI/sign_up.html)
3. [User Login](https://gtsofa.github.io/StackOverflowLite/UI/log_in.html)
4. [User Profile Page](https://gtsofa.github.io/StackOverflowLite/UI/user_profile.html)
5. [Post a question page](https://gtsofa.github.io/StackOverflowLite/UI/questions.html)
6. [View questions and answers page](https://gtsofa.github.io/StackOverflowLite/UI/questions_answers.html)

#### StackOverFlowLite Complete UI template on gh-pages

* [gh-pages link](https://gtsofa.github.io/StackOverflowLite/UI/)

#### Getting started

The following instructions will get a copy of StackOverFlowLite up and running on your machine for development and testing purposes

#### Requirements
StackOverFlowLite will require the following:

* A computer running on any distribution of Unix or Mac or Windows OS

#### Installation

```bash
# Clone the repository to your local machine
$ git clone https://github.com/gtsofa/StackOverflowLite.git
# Navigate to the directory
$ cd StackOverflowLite/UI
# Open the file
$ Open index.html file with a browser of your choice
```



### Challenge 2 - Create API endpoints

#### Getting started

The following instructions will get a copy of StackOverFlowLite up and running on your machine for development and testing purposes

#### Requirements

StackOverFlowLite will require the following:

* A computer running on any distribution of Unix or Mac 
  If you're using Windows OS get some help from your administrator on how to install the application
* Python 3.5 or higher
* Pip
* Git
* Virtualenv 

#### Installation

To clone and run this application, you will need [Git](https://git-scm.com/) installed on your computer. From your command line:

```bash
# Clone this repository to your local machine
$ git clone https://github.com/gtsofa/StackOverflowLite.git

# Navigate to the folder that contains the app
$ cd StackOverflowLite

# Create a virtual environment and activate it
$ virtualenv -p python3 venv

# Activate the virtual environment
$ source venv/bin/activate

# Install the requirements
$ pip install -r requirements.txt

# Launch the application
$ python3 run.py

### Run the tests
$ nosetests --with-coverage
```

#### API endpoints

#### Users Endpoints

Method | Endpoint | Functionality
--- | --- | ---
POST | /StackOverFlowLite/api/v1/auth/register | Creates a user account
POST | /StackOverFlowLite/api/v1/auth/login | Logs in a user
POST | /StackOverFlowLite/api/v1/auth/logout | Logs out a user
PUT | /StackOverFlowLite/api/v1/auth/reset-password | Reset a password for a logged user
DELETE | /StackOverFlowLite/api/v1/questions/question-ID | Delete a request of a logged in user

#### Questions Endpoints

Method | Endpoint | Functionality
--- | --- | ---
POST | /StackOverFlowLite/api/v1/questions | Add a question
POST | /StackOverFlowLite/api/v1/questions/question-ID/answers | Add an answer
GET | /StackOverFlowLite/api/v1/questions | Lists all questions 
GET | /StackOverFlowLite/api/v1/questions/questionID | List a question 
PUT | /StackOverFlowLite/api/v1/questions/questionID | Edit a question of a logged in user
DELETE | /StackOverFlowLite/api/v1/questions/questionID | Delete a request of a logged in user

#### Answers Endpoints

Method | Endpoint | Functionality
--- | --- | ---
POST | /StackOverFlowLite/api/v1/questions/question-ID/answers | Add an answer
GET | /StackOverFlowLite/api/v1/questions/questionID/answers | Lists all answers 
PUT | /StackOverFlowLite/api/v1/questions/questionID/answer/answerID | Edit an answer 
DELETE | /StackOverFlowLite/api/v1/questions/questionID/answer/answerID | Delete an answer


### Challenge 3 - Create more API endpoints and integrate a database

#### Required Features
1. Create user account that can sign in the app
2. Create user account that can sign out of the app
3. A user can get all questions
4. A user can get a single question
5. A user can post a question
6. A user can delete a question
7. A user can post an answer to a question
8. A user can mark an answer as preferred
9. A user can fetch all questions he or she has ever asked on the platform

### Endpoints for challenge 3

Method | Endpoint | Functionality
--- | --- | ---
POST | /StackOverFlowLite/api/v2/auth/signup | Register a user
POST | /StackOverFlowLite/api/v2/auth/login | Logs in a user
GET | /StackOverFlowLite/api/v2/questions | Fetches all questions
GET | /StackOverFlowLite/api/v2/questions/questionID | Fetches a specific question
POST | /StackOverFlowLite/api/v2/questions | Post a question
DELETE | /StackOverFlowLite/api/v2/questions/questionID | Delete a question
POST | /StackOverFlowLite/api/v2/questions/questionID/answer | Post an answer to a question 
PUT | /StackOverFlowLite/api/v2/questions/questionID/answers/answerID | Mark an answer as an acepted



#### StackOverFlowLite hosted on Heroku
* [stackoverflowlite V1 on Heroku](https://gtsofastackoverflowlite.herokuapp.com/api/v1)
* [stackoverflowlite V2 on Heroku](https://gtsofastackoverflowlite.herokuapp.com/api/v2)

### Screenshots

user register


#### Build with
* HTML, CSS, Javascript
* Flask RESTful API

#### How to Contribute
1. Fork the repository to your github account
2. Create a branch
3. Make changes
4. Create a pull request

#### License 
The software is protected under [MIT License](https://github.com/gtsofa/StackOverflowLite/blob/master/LICENSE)

#### Contributors
* [Julius Nyule](https://github.com/gtsofa)





