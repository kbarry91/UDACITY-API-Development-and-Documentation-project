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

        self.DB_NAME = os.environ.get('DB_NAME')
        self.DB_USER = os.environ.get('DB_USER')
        self.DB_PASSWORD = os.environ.get('DB_PASSWORD')
        self.DB_HOST = os.environ.get('DB_HOST')
        self.DB_PORT = os.environ.get('DB_PORT')
        self.DB_PATH = "postgres://{}:{}@{}:{}/{}".format(
        self.DB_USER, self.DB_PASSWORD, self.DB_HOST, self.DB_PORT, self.DB_NAME)
       



        #self.database_name = "trivia_test"
        #self.user = "postgres"
        #password = 'postgres'
        #self.host = 'localhost'
        #self.port = '5432'
        #self.database_path = "postgres://{}:{}@{}:{}/{}".format(
        #    self.user, password, self.host, self.port, self.database_name)
        setup_db(self.app, self.DB_PATH)

        # Test Data
        self.categories = {'1': 'Science', '2': 'Art', '3': 'Geography',
                           '4': 'History', '5': 'Entertainment', '6': 'Sports'}

        self.new_question = {
            'question': 'Is this another a new test question?',
            'answer': 'Yes',
            'difficulty': 1,
            'category': 1
        }

        self.invalid_question = {
            'question': 'Is this another a new test question?',
            'difficulty': 1,
        }

        self.search_term = {
            'searchTerm': 'Which'
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

    def test_retrieve_categories(self):
        """Test that categories are returned"""
        res = self.client().get('/api/v1/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertDictEqual(data['categories'], self.categories)

    def test_retrieve_questions(self):
        """Test paginated questions returned"""
        res = self.client().get('/api/v1/questions?page=1')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['questions'])
        self.assertTrue(data['total_questions'])
        self.assertTrue(len(data['questions']) <= 10)

    def test_422_retrieve_questions_invalid_page(self):
        """ Test invalid page range returns 422 error """
        res = self.client().get('/api/v1/questions?page=100')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data["message"], "Unprocessable Entity")

    def test_delete_question(self):
        """ Test question is deleted """
        question_id = self.util_add_question()

        res = self.client().delete('/api/v1/questions/{}'.format(question_id))
        data = json.loads(res.data)
        question = Question.query.filter(
            Question.id == question_id).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['deleted'], question_id)
        self.assertEqual(data['success'], True)
        self.assertEqual(question, None)

    def test_404_delete_question_does_not_exist(self):
        """ Test deleting question that doesnt exist returns error"""
        res = self.client().delete('/api/v1/questions/500')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)

    def test_add_question(self):
        """ Test add questions adds a new questions and returns a new id."""
        res = self.client().post("/api/v1/questions", json=self.new_question)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["new_question"])

        # Clean up
        self.util_delete_question(data['new_question'])

    def test_400_add_question_incomplete_request(self):
        """ Test add questions does not add question if incomplete request."""
        res = self.client().post("/api/v1/questions", json=self.invalid_question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "bad request")

    def test_retrieve_questions_by_search_found(self):
        """ Test search questions based on a search term returns result."""
        res = self.client().post("/api/v1/questions/search", json=self.search_term)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(data['questions'])
        self.assertEqual(data['total_questions'], 7)

    def test_retrieve_questions_by_search_not_found(self):
        """ Test search questions based on a search term."""
        res = self.client().post("/api/v1/questions/search",
                                 json={"searchTerm": "NOT FOUND"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(len(data['questions']), 0)
        self.assertEqual(data['total_questions'], 0)

    def test_retrieve_questions_with_category_id(self):
        """ Test retrieve questions based on category id."""

        res = self.client().get("/api/v1/categories/1/questions?page=1")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["questions"])
        self.assertTrue(data["total_questions"])
        self.assertEqual(data["current_category"], 1)

    def test_retrieve_questions_with_invalid_category_id(self):
        """ Test retrieve questions based on invalid category id."""

        res = self.client().get("/api/v1/categories/999/questions?page=1")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "Resource not found")

    def test_play_quiz_get_next_question(self):
        """ Test retrieve next question available."""

        res = self.client().post("api/v1/quizzes",
                                 json={
                                     "previous_questions": [16, 17],
                                     "quiz_category": {
                                         "id": "2",
                                         "type": "Art"}})
        data = json.loads(res.data)
        self.assertTrue(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["question"])

    def test_play_quiz_no_next_question(self):
        """ Test retrieve next question not available."""

        res = self.client().post("api/v1/quizzes", json={
            "previous_questions": [16, 17, 18, 19],
            "quiz_category": {"id": "2", "type": "Art"}
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertEqual(data["question"], None)

    def util_delete_question(self, question_id):
        """ Util function to delete a question."""
        res = self.client().delete('/api/v1/questions/{}'.format(question_id))
        data = json.loads(res.data)

    def util_add_question(self):
        """ Util function to add a question."""
        res = self.client().post('/api/v1/questions', json=self.new_question)
        data = json.loads(res.data)
        question_id = data['new_question']

        return question_id


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
