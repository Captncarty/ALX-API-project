# Backend - Trivia API

## Setting up the Backend

### Install Dependencies

1. **Python 3.7** - Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

2. **Virtual Environment** - We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organized. Instructions for setting up a virual environment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

3. **PIP Dependencies** - Once your virtual environment is setup and running, install the required dependencies by navigating to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

#### Key Pip Dependencies

- [Flask](http://flask.pocoo.org/) is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use to handle the lightweight SQL database. You'll primarily work in `app.py`and can reference `models.py`.

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross-origin requests from our frontend server.

### Set up the Database

With Postgres running, create a `trivia` database:

```bash
createbd trivia
```

Populate the database using the `trivia.psql` file provided. From the `backend` folder in terminal run:

```bash
psql trivia < trivia.psql
```

### Run the Server

From within the `./src` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
flask run --reload
```

The `--reload` flag will detect file changes and restart the server automatically.

## To Do Tasks

These are the files you'd want to edit in the backend:

1. `backend/flaskr/__init__.py`
2. `backend/test_flaskr.py`

One note before you delve into your tasks: for each endpoint, you are expected to define the endpoint and response data. The frontend will be a plentiful resource because it is set up to expect certain endpoints and response data formats already. You should feel free to specify endpoints in your own way; if you do so, make sure to update the frontend or you will get some unexpected behavior.

1. Use Flask-CORS to enable cross-domain requests and set response headers.
2. Create an endpoint to handle `GET` requests for questions, including pagination (every 10 questions). This endpoint should return a list of questions, number of total questions, current category, categories.
3. Create an endpoint to handle `GET` requests for all available categories.
4. Create an endpoint to `DELETE` a question using a question `ID`.
5. Create an endpoint to `POST` a new question, which will require the question and answer text, category, and difficulty score.
6. Create a `POST` endpoint to get questions based on category.
7. Create a `POST` endpoint to get questions based on a search term. It should return any questions for whom the search term is a substring of the question.
8. Create a `POST` endpoint to get questions to play the quiz. This endpoint should take a category and previous question parameters and return a random questions within the given category, if provided, and that is not one of the previous questions.
9. Create error handlers for all expected errors including 400, 404, 422, and 500.

## Documenting your Endpoints

You will need to provide detailed documentation of your API endpoints including the URL, request parameters, and the response body. Use the example below as a reference.

## API endpoints documentation

`GET '/categories'`

- This endpoint queries the database for all the available categories in the application which is formatted as a dictionary where the ids of the categories serve as keys and the category type serve as values.
- Request Arguments: None
- Returns: An object with the keys; `success`, `message`, `categories`, `category_count`.
Below is the object it returns.

```json
{
  "success": "True",
  "message": "Categories fetched successfully",
  "categories": {
      "1": "Science",
      "2": "Art",
      "3": "Geography",
      "4": "History",
      "5": "Entertainment",
      "6": "Sports"
    },
  "categories_count": 6
}
```

- When this request fails, an error report is returned to the user. This is a BAD_REQUEST error (400),
the error body is returned as 

```json
{
  "success": "False",
  "message": "Bad request, please check your request",
  "error": 400
}
```

`GET '/questions'`

- This endpoint queries the database and returns all the questions available in the database. These questions are paginated by 10 questions per page. In that case, it accepts a query (page=1, where can be any number as long as it doesn't exceed the available pages.) although if the argument is not passed, it returns just the first page.
- Request Argument: None.
- Returns: An object with the keys; `success`, `questions`, `questions_count`, `categories`, `curerent_category`, `message`

```json
{
  "success": "True",
  "message": "Questions fetched successfully",
  "questions": [
      {
      "answer": "Tom Cruise", 
      "category": 5, 
      "difficulty": 4, 
      "id": 4, 
      "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
    }, 
    {
      "answer": "Maya Angelou", 
      "category": 4, 
      "difficulty": 2, 
      "id": 5, 
      "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
    }, 
    {
      "answer": "Edward Scissorhands", 
      "category": 5, 
      "difficulty": 3, 
      "id": 6, 
      "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
    }, 
    {
      "answer": "Muhammad Ali", 
      "category": 4, 
      "difficulty": 1, 
      "id": 9, 
      "question": "What boxer's original name is Cassius Clay?"
    }, 
    {
      "answer": "Brazil", 
      "category": 6, 
      "difficulty": 3, 
      "id": 10, 
      "question": "Which is the only team to play in every soccer World Cup tournament?"
    }
  ],
  "questions_count": 20,
  "current_category": "Science",
  "categories": {
      "1": "Science",
      "2": "Art",
      "3": "Geography",
      "4": "History",
      "5": "Entertainment",
      "6": "Sports"
  }
}
```

- When this request fails, maybe due to request for an unavailable page, an error report is returned;

```json
{
  "success": "False",
  "message": "Not Found, Item not found",
  "error": 404
}
```

`DELETE '/questions/20'`

- This endpoint deletes a question from the database. It searches for the question and deletes it.
- Request Argument: question id.
- Returns: An object with the keys; `success`, `message`

```json
{
  "success": "True",
  "message": "Question deleted Successfuly"
}
```
-If this request fails (most times it's because the question wasn't found), it return an error report.

```json
{
  "success": "False",
  "message": "Not Found, Item not found",
  "error": 404
}
```

`POST '/questions'`

- This endpoint creates a new question and stores it into the questions table in the database.
- payloads: {
  'question': 'What is the name of....',
  'answer': 'Random Answer',
  'difficulty': 4,
  'category': 2
} 
- Request Argument: None
- Returns: An object with the keys; `success`, `message`, `created`, `question`

```json
{
  "success": "True",
  "message": "Questions fetched successfully",
  "created": 4, "(question Id)"
  "question": {
      "answer": "Tom Cruise", 
      "category": 5, 
      "difficulty": 4, 
      "id": 4, 
      "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
    },
       
}
```

-If this request fails, it return an error report.

```json
{
  "success": "False",
  "message": "Cannot proccess, please check your payload (request)",
  "error": 422
}
```

`GET '/categories/2/questions'`

- This endpoint gets questions based on categories.
- Request Argument: category id (number)
- Returns: An object with the keys; `success`, `message`, `questions`, `total_questions`, `current_category`

```json
{
  "success": "True",
  "message": "Questions fetched successfully",
  "questions": [
    {
      "answer": "Tom Cruise", 
      "category": 5, 
      "difficulty": 4, 
      "id": 4, 
      "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
    },
    {
      "answer": "Tom Cruise", 
      "category": 5, 
      "difficulty": 4, 
      "id": 4, 
      "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
    },
    {
      "answer": "Tom Cruise", 
      "category": 5, 
      "difficulty": 4, 
      "id": 4, 
      "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
    },
  ],
  "total_questions": 4,
  "current_category": "History",
}
```

`POST '/questions'`

- This api endpoint fetches searched questions, its so similar to the endpoint for adding new question just that the payload for this is an object with one property (searchTerm). The search term doesn't have to be exactly what's in database, the database fetches everything that has the search term in it.
- payload: {
  "searchTerm": 'question"
}
- Request Argument: None
- Returns: An object with the keys; `success`, `questions`, `questions_count`, `curerent_category`, `message`

```json
{
  "success": "True",
  "message": "Questions fetched successfully",
  "questions": [
      {
      "answer": "Tom Cruise", 
      "category": 5, 
      "difficulty": 4, 
      "id": 4, 
      "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
    }, 
    {
      "answer": "Maya Angelou", 
      "category": 4, 
      "difficulty": 2, 
      "id": 5, 
      "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
    }, 
    {
      "answer": "Edward Scissorhands", 
      "category": 5, 
      "difficulty": 3, 
      "id": 6, 
      "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
    }, 
    {
      "answer": "Muhammad Ali", 
      "category": 4, 
      "difficulty": 1, 
      "id": 9, 
      "question": "What boxer's original name is Cassius Clay?"
    }, 
    {
      "answer": "Brazil", 
      "category": 6, 
      "difficulty": 3, 
      "id": 10, 
      "question": "Which is the only team to play in every soccer World Cup tournament?"
    }
  ],
  "questions_count": 20,
  "current_category": "Science"
}
```

`POST '/quizzes'`

- This endpoint fetches quizzes for the player to answer and get answers at the end. This endpoint fetches random questions from the database on users request.
- payload: {
  "previous_question": [12, 30, 1, 20],
  "category": 2
}
- Request Argument: None
- Returns: An object with the keys; `success`, `question`

```json
{
  "success": "True",
  "question": {
    {
      "answer": "Brazil", 
      "category": 6, 
      "difficulty": 3, 
      "id": 10, 
      "question": "Which is the only team to play in every soccer World Cup tournament?"
    }
  }
}
```

## Testing

Write at least one test for the success and at least one error behavior of each endpoint using the unittest library.

To deploy the tests, run

```bash
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```
