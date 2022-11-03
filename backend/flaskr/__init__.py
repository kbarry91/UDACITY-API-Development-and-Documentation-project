import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10
ALL_CATEGORIES = 0


def create_app(test_config=None):
    print("Launching Trivia Quiz API !")
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    CORS(app, resources={r"/api/v1*": {"origins": "*"}})

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers',
                             'GET, POST, PATCH, DELETE, OPTIONS')
        return response

    @app.route('/api/v1/categories', methods=['GET'])
    def retrieve_categories():
        """
        GET endpoint to handle  request for all available categories.
        Returns: a list of categories.
        """
        try:
            categories = Category.query.order_by(Category.type).all()
            formatted_categories = {
                category.id: category.type for category in categories}
            if len(categories) == 0:
                abort(404)
            return jsonify(
                {
                    "success": True,
                    "categories": formatted_categories,
                })
        except Exception:
            abort(422)

    @app.route('/api/v1/questions', methods=['GET'])
    def retrieve_questions():
        """
        GET endpoint to retrieve all questions paginated by 10 pages.
        Returns: a list of questions, number of total questions, current category and categories.
        """
        try:
            page = request.args.get('page', 1, type=int)

            questions = Question.query.order_by(Question.id).paginate(
                page=page, per_page=QUESTIONS_PER_PAGE)
            formatted_questions = [question.format()
                                   for question in questions.items]

            categories = Category.query.order_by(Category.id).all()
            formatted_categories = {
                category.id: category.type for category in categories}

            if len(formatted_questions) == 0:
                abort(404)
            return jsonify(
                {
                    "success": True,
                    "questions": formatted_questions,
                    "total_questions": questions.total,
                    "categories": formatted_categories,
                    "current_category": None,
                })
        except Exception:
            abort(422)

    @app.route('/api/v1/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):
        """
        DELETE endpoint to handle  request to delete question.
        Returns: a success response.
        """
        try:
            question = Question.query.filter(
                Question.id == question_id).one_or_none()

            # Confirm Question is populated
            if question is None:
                abort(404)

            Question.delete(question)

            return jsonify(
                {
                    "success": True,
                    "deleted": question_id
                })

        except Exception as e:
            if '404' in str(e):
                abort(404)
            else:
                abort(422)

    @app.route('/api/v1/questions', methods=['POST'])
    def add_question():
        """
        POST endpoint to add a new question.
        Returns: A success message.
        """
        # Get question data from request.
        try:
            new_question = request.get_json().get('question', None).strip()
            new_answer = request.get_json().get('answer', None).strip()
            new_difficulty = request.get_json().get('difficulty', None)
            new_category = request.get_json().get('category', None)
        except:
            abort(400)

        # Validate question data is populated.
        if (len(new_question) == 0 or len(new_answer) == 0 or new_difficulty is None or new_category is None):
            abort(400)

        # Create new Question Object.
        question = Question(
            question=new_question,
            answer=new_answer,
            category=new_category,
            difficulty=new_difficulty)

        try:
            question.insert()
            return jsonify({
                'success': True,
                'new_question': question.id,
            })
        except Exception as e:
            if '400' in str(e):
                abort(400)
            else:
                abort(422)

    @app.route('/api/v1/questions/search', methods=['POST'])
    def retrieve_questions_by_search():
        """
        POST endpoint to search questions based on a search term.
        Returns: A list of questions, total number of questions and current category.
        """
        try:
            # Get search_term from request body and trim leading and trailing whitespace
            search_term = request.get_json().get('searchTerm', None).strip()
        except:
            abort(400)

        try:
            questions = Question.query \
                .order_by(Question.id) \
                .filter(Question.question.ilike('%{}%'.format(search_term)))
            questions_formatted = [
                question.format() for question in questions
            ]

            return jsonify({
                'success': True,
                'questions': questions_formatted,
                'total_questions': len(questions_formatted),
                'current_category': None,
            })

        except Exception as e:
            if '400' in str(e):
                abort(400)
            else:
                abort(422)

    @app.route('/api/v1/categories/<int:category_id>/questions', methods=['GET'])
    def retrieve_questions_by_category(category_id):
        """
        GET endpoint to return questions based on a category_id parameter.
        Returns: A list of questions, total number of questions and current category.
        """
        try:
            page = request.args.get('page', 1, type=int)

            questions = Question.query.order_by(Question.id).filter(
                Question.category == category_id).paginate(page=page, per_page=QUESTIONS_PER_PAGE)
            formatted_questions = [question.format()
                                   for question in questions.items]

            if len(formatted_questions) == 0:
                abort(404)

            return jsonify(
                {
                    "success": True,
                    "questions": formatted_questions,
                    "total_questions": questions.total,
                    "current_category": category_id,
                })

        except Exception as e:
            if '404' in str(e):
                abort(404)
            else:
                abort(422)

    @app.route('/api/v1/quizzes', methods=['POST'])
    def play_quiz():
        """
        POST endpoint to play quiz.Takes a category and previous question parameters.
        Returns: next random question to be played for the quiz.
        """
        try:
            # Get raw request data.
            questions = None
            request_body = request.get_json()
            quiz_category = request_body.get('quiz_category', None)
            quiz_category_id = quiz_category.get('id')
            previous_qs = request_body.get('previous_questions', None)

            # Get all questions.
            if (quiz_category_id == ALL_CATEGORIES):
                questions = Question.query.all()
            else:
                questions = Question.query.filter(
                    Question.category == quiz_category_id).all()

            # Format questions.
            formatted_questions = [question.format() for question in questions]

            # Get ids of questions.
            all_question_ids = [question.get("id")
                                for question in formatted_questions]

            # Remove previous questions.
            valid_question_ids = [
                question for question in all_question_ids if question not in previous_qs]

            if (len(valid_question_ids) == 0):
                return jsonify({
                    'success': True,
                    'previousQuestions': previous_qs,
                    'question': None
                })
            else:
                new_current_question = Question.query.get(
                    random.choice(valid_question_ids))
                return jsonify({
                    'success': True,
                    'question': new_current_question.format()
                })

        except Exception:
            abort(422)

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "Resource not found"
        }), 404

    @app.errorhandler(422)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "Unprocessable Entity"
        }), 422

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "bad request"
        }), 400

    @app.errorhandler(405)
    def not_found(error):
        return (jsonify({
            "success": False,
            "error": 405,
            "message": "method not allowed"
        }), 405,)

    return app
