import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = f'postgresql://postgres:abc@127.0.0.1:5432/{self.database_name}'
        setup_db(self.app, self.database_path)

        self.new_question = {
            "answer": "Mecury", 
            "category": 1, 
            "difficulty": 2,  
            "question": "What is the first planet?"
        }

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    def test_categories_fetch_success(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['categories'])
        self.assertTrue(data['categories_count'])
        self.assertEqual(data['message'], 'Categories fetched successfully')

    def test_category_fetch_error(self):
        res = self.client().get('/categorie')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'])
        self.assertTrue(data['error'])

    def test_questions_fetch_success(self):
        res = self.client().get('/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['qusetions'])
        self.assertTrue(data['questions_count'])
        self.assertTrue(data['current_category'])
        self.assertEqual(data['message'], 'Questions fetched successfully')

    def test_questions_fetch_error_wrong_pagination(self):
        res = self.client().get('/questions?page=1000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Bad request, please check your request')
        self.assertTrue(data['error'])

    def test_question_delete_success(self):
        res = self.client().delete('/questions/36')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['message'])

    def test_question_delete_error(self):
        res = self.client().delete('/questions/10000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'])

    def test_create_new_question_success(self):
        res = self.client().post('/questions', json=self.new_question)
        data = json.loads(res.data)

        self.assertEqual(data['success'], True)
        self.assertTrue(data['message'])
        self.assertTrue(data['created'])
        self.assertTrue(data['question'])

    def test_create_new_question_error_wrong_url(self):
        res = self.client().post('/questions/2', json=self.new_question)
        data = json.loads(res.data)

        self.assertEqual(data['success'], False)
        self.assertEqual(res.status_code, 405)
        self.assertTrue(data['message'])

    def test_create_new_question_error_no_data(self):
        res = self.client().post('/questions')
        data = json.loads(res.data)

        self.assertEqual(data['success'], False)
        self.assertEqual(res.status_code, 422)
        self.assertTrue(data['message'])

    def test_create_new_question_error_no_data(self):
        res = self.client().post('/questions')
        data = json.loads(res.data)

        self.assertEqual(data['success'], False)
        self.assertEqual(res.status_code, 422)
        self.assertTrue(data['message'])

    def test_fetch_questions_by_category_success(self):
        res = self.client().post('/categories/1/questions')
        data = json.loads(res.data)

        self.assertEqual(data['success'], True)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['questions'])
        self.assertTrue(data['total_questions'])
        self.assertTrue(data['current_category'])


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()