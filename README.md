# API Development and Documentation Final Project

## Trivia App
This project was developed as part of The Udacity API documentation and Development course. The repo herein contains a React front end application and Flask backend server that connects to a POSTGRES database using SQLAlchemy. 

The main file that defines the API is [here.](./backend/__init__.py)

### Project Objective
Udacity is invested in creating bonding experiences for its employees and students. A bunch of team members got the idea to hold trivia on a regular basis and created a webpage to manage the trivia app and play the game, but their API experience is limited and still needs to be built out.

That's where you come in! Help them finish the trivia app so they can start holding trivia and seeing who's the most knowledgeable of the bunch. The application must:

1. Display questions - both all questions and by category. Questions should show the question, category and difficulty rating by default and can show/hide the answer.
2. Delete questions.
3. Add questions and require that they include question and answer text.
4. Search for questions based on a text query string.
5. Play the quiz game, randomizing either all questions or within a specific category.

Completing this trivia app will give you the ability to structure plan, implement, and test an API - skills essential for enabling your future applications to communicate with others.

## Frontend

The [frontend](./frontend/README.md) directory contains a complete React frontend to consume the data from the Flask server. 

To start the React app, from the frontend directory run: 

```bash
npm start
```

> View the [Frontend README](./frontend/README.md) for more details.

## Backend
### Install Dependencies

1. **Python 3.7** - Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

2. **Virtual Environment** - We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organized. Instructions for setting up a virual environment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

3. **PIP Dependencies** - Once your virtual environment is setup and running, install the required dependencies by navigating to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

### Set up POSTGRES Database
- Install postgres

- With Postgres running, create a `trivia` database:

```bash
createdb trivia
```

- Populate the database using the `trivia.psql` file provided. From the `backend` folder in terminal run:

```bash
psql trivia < trivia.psql
```

### Run the flask Server

Secrets are stored as environment variables on your local machine and must be imported using `os.eniron.get('EXPECTED_ENV_VAR')`. To set the environment variables on Windows:
(NB. Replace `postgres_user` and `postgres_password` with your user name and password)
```bash
export DB_NAME=trivia
export DB_USER=postgres_user
export DB_PASSWORD=postgres_password
export DB_HOST=localhost
export DB_PORT=5432
```

To run the app on a Windows machine:
```bash
$ export FLASK_APP=flaskr
$ export FLASK_ENV=development
$ python -m flask run --reload
```
> View the [Backend README](./backend/README.md) for more details.

## Testing

Testing is done using the unittest library.
### Set up test database
- To Create Testing Database
With POSTGRES running:

```bash
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
```
### Set up Test Database environment variables
 To set the environment variables on Windows:
(NB. Replace `postgres_user` and `postgres_password` with your user name and password)
```bash
export DB_NAME=trivia_test
export DB_USER=postgres_user
export DB_PASSWORD=postgres_password
export DB_HOST=localhost
export DB_PORT=5432
```

### To Run the testing suite
The testing suite is located in the test_flaskr.py file.


To run the tests navigate to the backend directory and enter :

```bash
python test_flaskr.py
```

### To Run a specific test
To run specific test specify the class name and the test e.g.:

```bash
python test_flaskr.py TriviaTestCase.test_404_delete_question_does_not_exist
```
## API Reference

### Getting Started
- Base URL: At present this app can only be run locally and is not hosted as a base URL. The backend app is hosted at the default, `http://127.0.0.1:5000/`, which is set as a proxy in the frontend configuration. 
- Authentication: This version of the application does not require authentication or API keys. 

#### GET `'/api/v1/categories'`

- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Request Arguments: None
- Returns: An object with these keys:
  - `categories`: An object of `id: category_string` key: value pairs.
  - `success`: The success flag
```json
{
  "categories": {
    "1": "Science", 
    "2": "Art", 
    "3": "Geography", 
    "4": "History", 
    "5": "Entertainment", 
    "6": "Sports"
  }, 
  "success": true
}
```

#### GET `'/api/v1/questions?page=${integer}'`

- Request Arguments:
  `page`(int) -  current page
- Returns: An object with these keys:
  - `success`: The success flag
  - `questions`: A list of questions (paginated by 10 items)
  - `categories`: A dictionary of categories
  - `total_questions`: The total of questions
  - `current_category`: The current category

example: 
 `http://127.0.0.1:5000/api/v1/Fullyquestions?page=1`

```json
{
  "categories": {
    "1": "Science", 
    "2": "Art", 
    "3": "Geography", 
    "4": "History", 
    "5": "Entertainment", 
    "6": "Sports"
  }, 
  "current_category": null, 
  "success": true, 
  "total_questions": 19,
  "questions": [
    {
      "answer": "Agra", 
      "category": 3, 
      "difficulty": 2, 
      "id": 15, 
      "question": "The Taj Mahal is located in which Indian city?"
    }, 
    {
      "answer": "Escher", 
      "category": 2, 
      "difficulty": 1, 
      "id": 16, 
      "question": "Which Dutch graphic artist\u2013initials M C was a creator of optical illusions?"
    }
  ]
}
```

#### DELETE `'/api/v1/questions/<int:question_id>'`
- Send a delete request to delete a question based on the question ID.
- Request Arguments:
  `question_id`(int) -  ID of question to delete
- Returns(on success): An object with these keys:
  - `success`: The success flag
  - `deleted`: ID of deleted question
```json
{
    "success": True,
    "deleted": question_id
}
  ```
  - Returns(on failure): A 404 error if question is not found.


#### POST `'/api/v1/questions'`
- Sends a post request to add a new question.
 - Accepts a JSON request body:
    - `question`: The new question
    - `answer`: The answer for the question
    - `difficulty`: The difficulty
    - `category`: The category_id for the new question

 Returns(on success): An object with these keys:
  - `success`: The success flag
  - `new_question`: ID of the new question
```json
{
    "success": True,
    "new_question": question.id
}
  ```
  - Returns(on failure): A 400 error if all request information is not provided.

#### POST `'/api/v1/questions/search'`
- Sends post request to search for a question(s) by a provided search term. Strips trailing and leading whitespace from the search term
 - Accepts a JSON request body:
    - `searchTerm`: The string to search

- Returns(on success): An object with these keys:
  - `success`: The success flag
  - `questions`: A list of questions that match the search term
  - `total_questions`: The amount of questions returned
  - `current_category`: The category of the questions

```json
{
  "current_category": null, 
  "questions": [
    {
      "answer": "Tom Cruise", 
      "category": 5, 
      "difficulty": 4, 
      "id": 4, 
      "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
    }
  ], 
  "success": true, 
  "total_questions": 1
}
  ```
  - Returns(on failure): A 400 error if all request information is not provided.

#### GET `'/api/v1/categories/<int:category_id>/questions`
- Fetches questions based on a provided category#
- Accepts a parameter category_id provided in the URL
- Returns(on success): An object with these keys:
  - `success`: The success flag
  - `questions`: A list of questions that match the category
  - `total_questions`: The amount of questions returned
  - `current_category`: The category of the questions
```json
{
  "current_category": 6, 
  "questions": [
    {
      "answer": "Brazil", 
      "category": 6, 
      "difficulty": 3, 
      "id": 10, 
      "question": "Which is the only team to play in every soccer World Cup tournament?"
    }, 
    {
      "answer": "Uruguay", 
      "category": 6, 
      "difficulty": 4, 
      "id": 11, 
      "question": "Which country won the first ever soccer World Cup in 1930?"
    }
  ], 
  "success": true, 
  "total_questions": 2
}
```

- Returns(on failure): A 404 if no questions are found

#### POST `'/api/v1/quizzes'`
- Sends post request to play quiz .Takes a category and previous question parameters. If no category is provided will select questions from all categories. When no more questions are available the game is ended.
 - Accepts a JSON request body:
    - `quiz_category`: The string to search
    - `previous_questions`: List of previous questions already used in the quiz

- Returns(on success if more questions available): An object with these keys:
  - `success`: The success flag
  - `questions`: The next question to play

- Returns(on success if no more questions are available): An object with these keys:
  - `success`: True
  - `previousQuestions`: List of ID's of previously played questions
  - `question`: None 
```json
{
    "question": {
        "answer": "Blood",
        "category": 1,
        "difficulty": 4,
        "id": 22,
        "question": "Hematology is a branch of medicine involving the study of what?"
    },
    "success": true
}
```

## Error Handling

Errors are returned as json format: 
### 400 `Bad request`
```json
{ 
  "success": False, 
  "error": 400, 
  "message": 'bad request' 
}
```
### 404 `Not found`
```json
{ 
  "success": False, 
  "error": 404, 
  "message": 'Resource not found' 
}
```
### 422 `Unprocessable Entity`
```json
{ 
  "success": False, 
  "error": 422, 
  "message": 'Unprocessable Entity' 
}
```
### 405 `Method not allowed`
```json
{ 
  "success": False, 
  "error": 405, 
  "message": 'method not allowed' 
}
```