from crypt import methods
from email import message
import json
from nis import cat
import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    CORS(app)

    cors = CORS(app, resources={r"/*": {"origins": "*"}})

    # cors headers
    @app.after_request
    def after_request(response):
        response.headers.add("Access-Control-Allow-Headers", "Content-Type,Authorization")
        response.headers.add("Access-Control-Allow-Methods", "GET,PUT,POST,DELETE,OPTIONS,PATCH")
        return response


    @app.route('/categories', methods=['GET'])
    def categories():

        error = False
        
        try:
            categories = Category.query.order_by(Category.id.asc()).all()

            formated_categories = { category.id: category.type for category in categories }

            return jsonify({
                'success': True,
                'message': 'Categories fetched successfully',
                'categories': formated_categories,
                'categories_count': len(formated_categories)
            })

        except:
            error = True
            abort(400)


    @app.route('/questions', methods=['GET'])
    def questions():
        error = False

        try:
            page = request.args.get('page', 1, type=int)
            start = (page - 1) * QUESTIONS_PER_PAGE
            end = start + QUESTIONS_PER_PAGE

            # questions_category = request.args.get('category', 1, type=int)

            questions = Question.query.order_by(Question.id.asc()).all()
            formatted_question = [ question.format() for question in questions ]

            categories = Category.query.order_by(Category.id.asc()).all()
            # current_category = Category.query.filter(Category.id == questions_category).first()
            formated_categories = { category.id: category.type for category in categories }

            result = {
                'success': True,
                'message': 'Questions fetched successfully',
                'questions': formatted_question[start:end],
                'questions_count': len(formatted_question),
                'current_category': 'Science',
                'categories': formated_categories
            }

            if result['questions'] == []:
                abort(404)

            return jsonify(result)
        except:
            error = True
            abort(404)

    
    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):
        error = False

        try:
            question = Question.query.filter_by(id=question_id).first()

            if question is None:
                abort(404)
            else:
                question.delete()
                return jsonify({
                    'success': True,
                    'message': 'Question deleted Successfuly'
                })
        except:
            error = False
            abort(405)


    @app.route('/questions', methods=['POST'])
    def add_quetions():
        data = request.get_json()

        print(data)

        question = data.get('question')
        answer = data.get('answer')
        category = data.get('category')
        difficulty = data.get('difficulty')

        search = data.get('searchTerm')

        try:
            
            if data:
                if search:
                    results = Question.query.filter(Question.question.ilike('%'+ search +'%')).all()

                    return jsonify({
                        'success': True,
                        'questions': [ result.format() for result in results ],
                        'total_questions': len(results),
                        'current_category': 'Science'
                    })
                else:
                    if question is None:
                        return jsonify({
                            'success': False,
                            'message': 'Please provide a question'
                        })
                    
                    if answer is None:
                        return jsonify({
                            'success': False,
                            'message': 'Please provide an answer'
                        })

                    if category is None:
                        return jsonify({
                            'success': False,
                            'message': 'Please provide a category'
                        })

                    if difficulty is None:
                        return jsonify({
                            'success': False,
                            'message': 'Please provide a difficulty level'
                        })

                    newQuestion = Question(question=question, answer=answer, category=category, difficulty=difficulty)

                    if bool(Question.query.filter_by(question=question).first()):
                        return jsonify({
                            'message': 'Question already exist',
                            'success': False
                        })

                    newQuestion.insert()

                    return jsonify({
                        'success': True,
                        'message': 'Question added successfully',
                        'created': newQuestion.id,
                        'question': newQuestion.format(),
                    })
        except:
            abort(422)


    @app.route('/questions', methods=['POST'])
    def get_searched_questions():
        search_term = request.get_json()

        results = Question.query.filter(Question.question.ilike('%'+ search_term.get('searchTerm') +'%')).all()

        return jsonify({
            'success': True,
            'questions': [ result.format() for result in results ],
            'total_questions': len(results),
            'current_category': 'Science'
        })


    @app.route('/categories/<int:category_id>/questions', methods=['GET'])
    def questions_by_category(category_id):
        try:
            page = request.args.get('page', 1, type=int)
            start = (page - 1) * QUESTIONS_PER_PAGE
            end = start + QUESTIONS_PER_PAGE

            questions = Question.query.order_by(Question.id.asc()).filter(Question.category == category_id).all()
            formatted_question = [ question.format() for question in questions ]

            current_category = Category.query.filter(Category.id == category_id).first()

            return jsonify({
                'success': True,
                'message': 'Questions fetched successfully',
                'questions': formatted_question[start:end],
                'total_questions': len(formatted_question),
                'current_category': current_category.type,
            })
        except:
            error = True
            abort(400)


    @app.route('/quizzes', methods=['POST'])
    def get_quizzes():
        data = request.get_json()

        category = data.get('quiz_category').get('id')
        previous_questions = data.get('previous_questions')

        questions = []

        print(category)

        try:
            if category == 0:
                if len(previous_questions) == 0:
                    quiz_question = Question.query.filter(Question.id == random.randint(0, 10)).first()
                    # quiz_question.format()
                    print(quiz_question)
                else:
                    for questionId in previous_questions:
                        random_questions = Question.query.filter(Question.id != questionId).limit(5-len(previous_questions))
                        quiz_question = random_questions[random.randint(0, (5-len(previous_questions)))]
            else:
                if len(previous_questions) == 0:
                    quiz_question = Question.query.filter(Question.category == category).first()
                    # formatted_quiz = [ question.format() for question in quiz_questions ]

                    print(quiz_question)
                else:
                    for questionId in previous_questions:
                        quiz_questions = Question.query.filter(Question.category == category).filter(Question.id != questionId).limit(5-len(previous_questions))
                        quiz_question = quiz_questions[random.randint(0, (5-len(previous_questions)))]

            return jsonify({
                'success': True,
                'question': quiz_question.format()
            })
        except:
            abort(404)

    @app.errorhandler(400)
    def error400(error):
        return jsonify({
            'success': False,
            'message': 'Bad request, please check your request',
            'error': 400
        }), 400

    @app.errorhandler(404)
    def error404(error):
        return jsonify({
            'success': False,
            'message': 'Not Found, Item not found',
            'error': 404
        }), 404

    @app.errorhandler(405)
    def error405(error):
        return jsonify({
            'success': False,
            'message': 'Method not Allowed, please check your request',
            'error': 405
        }), 405

    @app.errorhandler(422)
    def error422(error):
        return jsonify({
            'success': False,
            'message': 'Cannot proccess, please check your payload (request)',
            'error': 422
        }), 422

    return app

