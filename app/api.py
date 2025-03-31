from flask import Blueprint, jsonify, request, abort
from sqlalchemy.orm import Session
from app import crud, schemas
from app.database import get_db
from app.llm_utils import generate_book_summary, generate_review_summary, generate_recommendations
from typing import List
import jwt
import datetime
import os

bp = Blueprint('api', __name__, url_prefix='/api')

@bp.route("/books", methods=["POST"])
def create_book():
    db: Session = get_db()
    book_data = request.get_json()
    book = schemas.BookCreate(**book_data)
    db_book = crud.create_book(db, book)
    return jsonify(schemas.Book.from_orm(db_book).dict()), 201

@bp.route("/books", methods=["GET"])
def read_books():
    db: Session = get_db()
    books = crud.get_books(db)
    return jsonify([schemas.Book.from_orm(book).dict() for book in books])

@bp.route("/books/<int:book_id>", methods=["GET"])
def read_book(book_id: int):
    db: Session = get_db()
    db_book = crud.get_book(db, book_id)
    if db_book is None:
        abort(404)
    return jsonify(schemas.Book.from_orm(db_book).dict())

@bp.route("/books/<int:book_id>", methods=["PUT"])
def update_book(book_id: int):
    db: Session = get_db()
    book_data = request.get_json()
    book_update = schemas.BookCreate(**book_data)
    db_book = crud.update_book(db, book_id, book_update)
    if db_book is None:
        abort(404)
    return jsonify(schemas.Book.from_orm(db_book).dict())

@bp.route("/books/<int:book_id>", methods=["DELETE"])
def delete_book(book_id: int):
    db: Session = get_db()
    deleted = crud.delete_book(db, book_id)
    if not deleted:
        abort(404)
    return jsonify({"message": "Book deleted"}), 200

@bp.route("/books/<int:book_id>/reviews", methods=["POST"])
def create_review(book_id: int):
    db: Session = get_db()
    review_data = request.get_json()
    review = schemas.ReviewCreate(**review_data)
    db_review = crud.create_book_review(db, book_id, review)
    return jsonify(schemas.Review.from_orm(db_review).dict()), 201

@bp.route("/books/<int:book_id>/reviews", methods=["GET"])
def read_reviews(book_id: int):
    db: Session = get_db()
    reviews = crud.get_book_reviews(db, book_id)
    return jsonify([schemas.Review.from_orm(review).dict() for review in reviews])

@bp.route("/books/<int:book_id>/summary", methods=["GET"])
def read_summary(book_id: int):
    db: Session = get_db()
    book = crud.get_book(db, book_id)
    if not book:
        abort(404)

    book_summary = book.summary if book.summary else generate_book_summary(book.title + " " + book.author + " " + book.genre)  # Generate summary using LLM
    reviews = crud.get_book_reviews(db, book_id)
    review_texts = [review.review_text for review in reviews]
    review_summary = generate_review_summary(review_texts) # Generate review summary

    average_rating = None
    if reviews:
        average_rating = sum(review.rating for review in reviews) / len(reviews)

    return jsonify({
        "book_summary": book_summary,
        "review_summary": review_summary,
        "average_rating": average_rating
    })

@bp.route("/recommendations", methods=["POST"])
def get_recommendations():
    db: Session = get_db()
    user_preferences = request.get_json().get("preferences")
    books = crud.get_books(db)
    books_data = [schemas.Book.from_orm(book).dict() for book in books]
    recommendations = generate_recommendations(user_preferences, books_data)
    return jsonify({"recommendations": recommendations})

@bp.route("/generate-summary", methods=["POST"])
def generate_summary():
    db: Session = get_db()
    book_content = request.get_json().get("content")
    summary = generate_book_summary(book_content)
    return jsonify({"summary": summary})

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'message': 'Token is missing!'}), 401

        try:
            data = jwt.decode(token, os.environ.get('SECRET_KEY'), algorithms=["HS256"])
            # You might want to fetch the user from the database here based on data['user_id']
        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Token has expired!'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'message': 'Token is invalid!'}), 401
        except Exception as e:
            return jsonify({'message': 'An error occurred while verifying the token!'}), 500

        return f(*args, **kwargs)

    return decorated

@bp.route('/login', methods=['POST'])
def login():
    auth = request.authorization

    if not auth or not auth.username or not auth.password:
        return jsonify({'message': 'Could not verify!'}), 401, {'WWW-Authenticate': 'Basic realm="Login required!"'}

    # Replace with your actual user authentication logic (e.g., database query)
    if auth.username == 'testuser' and auth.password == 'testpassword':
        token = jwt.encode({'user_id': 1, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)},
                           os.environ.get('SECRET_KEY'), algorithm="HS256")

        return jsonify({'token': token})

    return jsonify({'message': 'Could not verify!'}), 401, {'WWW-Authenticate': 'Basic realm="Login required!"'}
