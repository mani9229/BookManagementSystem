import pytest
from app import create_app, db
from app.config import TestingConfig

@pytest.fixture(scope='module')
def test_client():
    app = create_app(TestingConfig)  # Use the TestingConfig
    with app.test_client() as client:
        with app.app_context():
            db.create_all()  # Create tables
            yield client
            db.session.remove()
            db.drop_all()  # Drop tables after tests

@pytest.fixture(scope='module')
def auth_headers(test_client):
    #   Register a user for testing
    test_client.post('/api/register', json={'username': 'testuser', 'password': 'testpassword'})
    #   Login and get the token
    response = test_client.post('/api/login', json={'username': 'testuser', 'password': 'testpassword'})
    token = response.json['access_token']
    return {'Authorization': f'Bearer {token}'}

@pytest.fixture
def create_book(test_client, auth_headers):
    def _create_book(title='Test Book', author='Test Author', genre='Fiction'):
        data = {'title': title, 'author': author, 'genre': genre}
        return test_client.post('/api/books', json=data, headers=auth_headers)
    return _create_book

@pytest.fixture
def create_review(test_client, auth_headers, create_book):
    #   Ensure there's a book to review
    create_book()  # Create a default book
    def _create_review(book_id=1, review_text='Great book!', rating=5):
        data = {'review_text': review_text, 'rating': rating}
        return test_client.post(f'/api/books/{book_id}/reviews', json=data, headers=auth_headers)
    return _create_review