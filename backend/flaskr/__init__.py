import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10


def create_app(test_config=None):
    print("HELLO TRIVIA!!!")
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    """
    @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
    """
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    """
    @TODO: Use the after_request decorator to set Access-Control-Allow
    """
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers',
                             'GET, POST, PATCH, DELETE, OPTIONS')
        return response



   
    def paginate_books(request, selection):
        page = request.args.get("page", 1, type=int)
        start = (page - 1) * QUESTIONS_PER_PAGE
        end = start + QUESTIONS_PER_PAGE

        questions = [question.format() for question in selection]
        current_questions = questions[start:end]

        return current_questions

    @app.route('/api/v1/categories',methods=['GET'])
    def retrieve_categories():
        """
        GET endpoint to handle  request for all available categories.
        """
        try:
            categories = Category.query.order_by(Category.type).all()
            formatted_categories = {category.id: category.type for category in categories}
            if len(categories) == 0:
                abort(404)
            return jsonify(
                {
                    "success": True,
                    "categories": formatted_categories,
                })
        except Exception:
            abort(422)  
    """
    @TODO:
    Create an endpoint to handle GET requests for questions,
    including pagination (every 10 questions).
    This endpoint should return a list of questions,
    number of total questions, current category, categories.

    TEST: At this point, when you start the application
    you should see questions and categories generated,
    ten questions per page and pagination at the bottom of the screen for three pages.
    Clicking on the page numbers should update the questions.
    """
    @app.route('/api/v1/questions',methods=['GET'])
    def retrieve_questions():
        page = request.args.get('page',1,type=int)

        questions = Question.query.order_by(Question.id).paginate(page=page,per_page=QUESTIONS_PER_PAGE)
        formatted_questions = [question.format() for question in questions.items]
        
        categories = Category.query.order_by(Category.id).all()
        formatted_categories = {category.id: category.type for category in categories}
        
        if len(formatted_questions) == 0:
            abort(404)
        return jsonify(
            {
                "success": True,
                "questions": formatted_questions,
                "total_questions":questions.total,
                "categories": formatted_categories,
                "current_category": None,                

            })
    """
    @TODO:
    TEST: When you click the trash icon next to a question, the question will be removed.
    This removal will persist in the database and when you refresh the page.
    """
    @app.route('/api/v1/questions/<int:question_id>',methods=['DELETE'])
    def delete_question(question_id):
        """
        DELETE endpoint to handle  request to delete question.
        """
        try:
            question = Question.query.filter(Question.id == question_id).one_or_none()         
            print(question)
            #categories = Category.query.order_by(Category.type).all()
            #formatted_categories = {category.id: category.type for category in categories}
            #if len(categories) == 0:
            #    abort(404)
            return jsonify(
                {
                    "success": True,
                })
        except Exception:
            abort(422)  
    """
    @TODO:
    Create an endpoint to POST a new question,
    which will require the question and answer text,
    category, and difficulty score.

    TEST: When you submit a question on the "Add" tab,
    the form will clear and the question will appear at the end of the last page
    of the questions list in the "List" tab.
    """

    """
    @TODO:
    TEST: Search by any phrase. The questions list will update to include
    only question that include that string within their question.
    Try using the word "title" to start.
    """
    @app.route('/api/v1/questions',methods=['POST'])
    def retrieve_questions_by_search():
        """
        POST endpoint to search questions based on a search term  
        """    
        # Get search_term from request body and trim leading and trailing whitespace 
        search_term = request.get_json().get('searchTerm', None).strip()
       
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
        except Exception:
            abort(422)

    """
    @TODO:
    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    """
    @app.route('/api/v1/categories/<int:category_id>/questions',methods=['GET'])
    def retrieve_questions_by_category(category_id):
        """
        GET endpoint to return questions based on a category_id parameter.
        """
        try:
            page = request.args.get('page',1,type=int)

            questions = Question.query.order_by(Question.id).filter(Question.category == category_id).paginate(page=page,per_page=QUESTIONS_PER_PAGE)
            formatted_questions = [question.format() for question in questions.items]
 
            if len(formatted_questions) == 0:
                abort(404)

            return jsonify(
                {
                    "success": True,
                    "questions": formatted_questions,
                    "total_questions":questions.total,
                    "current_category": category_id,                

                })

        except Exception as e:
            if '404' in str(e):
                abort(404) 
            else:
                abort(422)
    """
    @TODO:
    Create a POST endpoint to get questions to play the quiz.
    This endpoint should take category and previous question parameters
    and return a random questions within the given category,
    if provided, and that is not one of the previous questions.

    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not.
    """

    """

    @TODO:
    Create error handlers for all expected errors
    including 404 and 422.
    """
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

    return app