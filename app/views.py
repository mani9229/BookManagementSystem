from flask import Blueprint, jsonify, request, abort
from app import db, jwt
from app.models import Book, Review, User
from app.schemas import BookSchema, ReviewSchema, UserSchema
from app.llm_utils import generate_book_summary, analyze_review_sentiment
from flasgger import swag_from, Swagger
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from marshmallow import ValidationError
from app.repositories import book_repository, review_repository  # Import repositories

bp = Blueprint('api', __name__, url_prefix='/api')

# Swagger setup
@bp.route('/swagger.json')
def swagger_json():
    from flask import jsonify
    from flasgger import LazyString, LazyJSONEncoder
    app = Flask(__name__)  # Create a temporary Flask app for Swagger
    app.json_encoder = LazyJSONEncoder
    swag = Swagger(app).get_swagger()
    return jsonify(swag)

@bp.route('/register', methods=['POST'])
@swag_from({
    'tags': ['Authentication'],
    'description': 'Register a new user',
    'requestBody': {
        'required': True,
        'content': {
            'application/json': {
                'schema': UserSchema(only=('username', 'password'))
            }
        }
    },
    'responses': {
        201: {
            'description': 'User created',
            'schema': UserSchema(only=('id', 'username'))
        },
        400: {
            'description': 'Invalid input or username already exists'
        }
    }
})
def register():
    data = request.get_json()
    user_schema = UserSchema(only=('username', 'password'))
    try:
        user_data = user_schema.load(data)
    except ValidationError as err:
        return jsonify({'errors': err.messages}), 400

    if User.query.filter_by(username=user_data['username']).first():
        return jsonify({'message': 'Username already exists'}), 400

    new_user = User(username=user_data['username'])
    new_user.set_password(user_data['password'])
    db.session.add(new_user)
    db.session.commit()
    return jsonify(UserSchema(only=('id', 'username')).dump(new_user)), 201

@bp.route('/login', methods=['POST'])
@swag_from({
    'tags': ['Authentication'],
    'description': 'Authenticate a user and get a JWT token',
    'requestBody': {
        'required': True,
        'content': {
            'application/json': {
                'schema': UserSchema(only=('username', 'password'))
            }
        }
    },
    'responses': {
        200: {
            'description': 'Login successful',
            'schema': {'type': 'object', 'properties': {'access_token': {'type': 'string'}}}
        },
        401: {
            'description': 'Invalid credentials'
        }
    }
})
def login():
    data = request.get_json()
    user_schema = UserSchema(only=('username', 'password'))
    try:
        user_data = user_schema.load(data)
    except ValidationError as err:
        return jsonify({'errors': err.messages}), 400

    user = User.query.filter_by(username=user_data['username']).first()
    if user and user.check_password(user_data['password']):
        access_token = create_access_token(identity=user.id)
        return jsonify({'access_token': access_token}), 200
    else:
        return jsonify({'message': 'Invalid credentials'}), 401

# Protect routes
@bp.route('/books', methods=['GET'])
@jwt_required()
@swag_from({
    'tags': ['Books'],
    'description': 'Get all books',
    'responses': {
        200: {
            'description': 'A list of books',
            'schema': BookSchema(many=True)
        },
        401: {
            'description': 'Authentication required'
        }
    }
})
def get_books():
    books = book_repository.get_all_books()
    book_schema = BookSchema(many=True)
    return jsonify(book_schema.dump(books))

@bp.route('/books/<int:book_id>', methods=['GET'])
@jwt_required()
@swag_from({
    'tags': ['Books'],
    'description': 'Get a single book by ID',
    'parameters': [
        {
            'name': 'book_id',
            'in': 'path',
            'type': 'integer',
            'required': True,
            'description': 'The ID of the book to retrieve'
        }
    ],
    'responses': {
        200: {
            'description': 'The book details',
            'schema': BookSchema
        },
        404: {
            'description': 'Book not found'
        },
        401: {
            'description': 'Authentication required'
        }
    }
})
def get_book(book_id):
    book = book_repository.get_book_by_id(book_id)
    if not book:
        return jsonify({'message': 'Book not found'}), 404
    book_schema = BookSchema()
    return jsonify(book_schema.dump(book))

@bp.route('/books', methods=['POST'])
@jwt_required()
@swag_from({
    'tags': ['Books'],
    'description': 'Create a new book',
    'requestBody': {
        'required': True,
        'content': {
            'application/json': {
                'schema': BookSchema
            }
        }
    },
    'responses': {
        201: {
            'description': 'Book created',
            'schema': BookSchema
        },
        400: {
            'description': 'Invalid input'
        },
        401: {
            'description': 'Authentication required'
        }
    }
})
def create_book():
    data = request.get_json()
    book_schema = BookSchema()
    try:
        book = book_schema.load(data)
    except ValidationError as err:
        return jsonify({'errors': err.messages}), 400
    new_book = book_repository.create_book(book)

    if not new_book.summary:
        new_book.summary = generate_book_summary(f"{new_book.title} by {new_book.author}. {new_book.genre}")
        book_repository.update_book(new_book.id, {'summary': new_book.summary})  # Update summary

    return jsonify(book_schema.dump(new_book)), 201

@bp.route('/books/<int:book_id>', methods=['PUT'])
@jwt_required()
@swag_from({
    'tags': ['Books'],
    'description': 'Update a book',
    'parameters': [
        {
            'name': 'book_id',
            'in': 'path',
            'type': 'integer',
            'required': True,
            'description': 'The ID of the book to update'
        }
    ],
    'requestBody': {
        'required': True,
        'content': {
            'application/json': {
                'schema': BookSchema(partial=True)
            }
        }
    },
    'responses': {
        200: {
            'description': 'Book updated',
            'schema': BookSchema
        },
        400: {
            'description': 'Invalid input'
        },
        404: {
            'description': 'Book not found'
        },
        401: {
            'description': 'Authentication required'
        }
    }
})
def update_book(book_id):
    book = book_repository.get_book_by_id(book_id)
    if not book:
        return jsonify({'message': 'Book not found'}), 404
    data = request.get_json()
    book_schema = BookSchema(partial=True)  # Allow partial updates
    try:
        updated_book_data = book_schema.load(data, instance=book)
    except ValidationError as err:
        return jsonify({'errors': err.messages}), 400
    updated_book = book_repository.update_book(book_id, updated_book_data)
    return jsonify(book_schema.dump(updated_book))

@bp.route('/books/<int:book_id>', methods=['DELETE'])
@jwt_required()
@swag_from({
    'tags': ['Books'],
    'description': 'Delete a book',
    'parameters': [
        {
            'name': 'book_id',
            'in': 'path',
            'type': 'integer',
            'required': True,
            'description': 'The ID of the book to delete'
        }
    ],
    'responses': {
        200: {
            'description': 'Book deleted',
            'schema': {'type': 'object', 'properties': {'message': {'type': 'string'}}}
        },
        404: {
            'description': 'Book not found'
        },
        401: {
            'description': 'Authentication required'
        }
    }
})
def delete_book(book_id):
    book = book_repository.get_book_by_id(book_id)
    if not book:
        return jsonify({'message': 'Book not found'}), 404
    book_repository.delete_book(book_id)
    return jsonify({'message': 'Book deleted'}), 200

@bp.route('/books/<int:book_id>/reviews', methods=['GET'])
@jwt_required()
@swag_from({
    'tags': ['Reviews'],
    'description': 'Get reviews for a book',
    'parameters': [
        {
            'name': 'book_id',
            'in': 'path',
            'type': 'integer',
            'required': True,
            'description': 'The ID of the book to get reviews for'
        }
    ],
    'responses': {
        200: {
            'description': 'A list of reviews',
            'schema': ReviewSchema(many=True)
        },
        404: {
            'description': 'Book not found'
        },
        401: {
            'description': 'Authentication required'
        }
    }
})
def get_book_reviews(book_id):
    book = book_repository.get_book_by_id(book_id)
    if not book:
        return jsonify({'message': 'Book not found'}), 404
    reviews = review_repository.get_reviews_by_book_id(book_id)
    review_schema = ReviewSchema(many=True)
    return jsonify(review_schema.dump(reviews))

@bp.route('/books/<int:book_id>/reviews', methods=['POST'])
@jwt_required()
@swag_from({
    'tags': ['Reviews'],
    'description': 'Add a review for a book',
    'parameters': [
        {
            'name': 'book_id',
            'in': 'path',
            'type': 'integer',
            'required': True,
            'description': 'The ID of the book to add a review to'
        }
    ],
    'requestBody': {
        'required': True,
        'content': {
            'application/json': {
                'schema': ReviewSchema(exclude=('user_id',))  # Exclude user_id from input
            }
        }
    },
    'responses': {
        201: {
            'description': 'Review created',
            'schema': ReviewSchema
        },
        400: {
            'description': 'Invalid input'
        },
        404: {
            'description': 'Book not found'
        },
        401: {
            'description': 'Authentication required'
        }
    }
})
def create_book_review(book_id):
    book = book_repository.get_book_by_id(book_id)
    if not book:
        return jsonify({'message': 'Book not found'}), 404
    data = request.get_json()
    review_schema = ReviewSchema(exclude=('user_id',))
    try:
        review_data = review_schema.load(data)
    except ValidationError as err:
        return jsonify({'errors': err.messages}), 400

    user_id = get_jwt_identity()  # Get the current user's ID from the JWT
    new_review = review_repository.create_review(book_id=book_id, user_id=user_id, review_text=review_data['review_text'], rating=review_data['rating'])
    return jsonify(ReviewSchema().dump(new_review)), 201

@bp.route('/books/<int:book_id>/summary', methods=['GET'])
@jwt_required()
@swag_from({
    'tags': ['Books'],
    'description': 'Get summary and aggregated rating for a book',
    'parameters': [
        {
            'name': 'book_id',
            'in': 'path',
            'type': 'integer',
            'required': True,
            'description': 'The ID of the book'
        }
    ],
    'responses': {
        200: {
            'description': 'Book summary and aggregated rating',
            'schema': {'type': 'object'}
        },
        404: {
            'description': 'Book not found'
        },
        401: {
            'description': 'Authentication required'
        }
    }
})
def get_book_summary(book_id):
    book = book_repository.get_book_by_id(book_id)
    if not book:
        return jsonify({'message': 'Book not found'}), 404
    reviews = review_repository.get_reviews_by_book_id(book_id)
    total_rating = sum(review.rating for review in reviews) if reviews else 0
    average_rating = total_rating / len(reviews) if reviews else 0
    return jsonify({
        'summary': book.summary,
        'average_rating': average_rating
    })

@bp.route('/recommendations', methods=['GET'])
@jwt_required()
@swag_from({
    'tags': ['Recommendations'],
    'description': 'Get book recommendations based on user preferences',
    'responses': {
        200: {
            'description': 'A list of book recommendations',
            'schema': BookSchema(many=True)  # Adjust schema as needed
        },
        401: {
            'description': 'Authentication required'
        }
    }
})
def get_recommendations():
    # to generate the recommendation we need to implement a recommendation engine or historical data so For now, i am returning all books as a simple example.
    books = book_repository.get_all_books()
    book_schema = BookSchema(many=True)
    return jsonify(book_schema.dump(books))

@bp.route('/generate-summary', methods=['POST'])
@jwt_required()
@swag_from({
    'tags': ['LLM'],
    'description': 'Generate a summary for a given book content',
    'requestBody': {
        'required': True,
        'content': {
            'application/json': {
                'schema': {'type': 'object', 'properties': {'text': {'type': 'string'}}}
            }
        }
    },
    'responses': {
        200: {
            'description': 'Generated summary',
            'schema': {'type': 'object', 'properties': {'summary': {'type': 'string'}}}
        },
        400: {
            'description': 'Invalid input'
        },
        401: {
            'description': 'Authentication required'
        }
    }
})
def generate_summary():
    data = request.get_json()
    if not data or 'text' not in data:
        return jsonify({'message': 'Invalid input. Provide "text" in the request body.'}), 400
    summary = generate_book_summary(data['text'])
    return jsonify({'summary': summary}), 200
