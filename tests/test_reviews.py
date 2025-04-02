import json

def test_create_review(test_client, auth_headers, create_book):
    #   Ensure there's a book to review
    create_book()

    data = {
        'review_text': 'This book was amazing!',
        'rating': 5
    }
    response = test_client.post('/api/books/1/reviews', json=data, headers=auth_headers)
    assert response.status_code == 201
    assert response.json['review_text'] == 'This book was amazing!'
    assert response.json['rating'] == 5

def test_get_book_reviews(test_client, auth_headers, create_book, create_review):
    #   Create a book and a review
    create_book()
    create_review()

    response = test_client.get('/api/books/1/reviews', headers=auth_headers)
    assert response.status_code == 200
    assert len(response.json) > 0
    assert response.json[0]['review_text'] == 'Great book!'

def test_create_review_invalid_data(test_client, auth_headers, create_book):
    #   Ensure there's a book to review
    create_book()

    data = {
        'review_text': 'This book was amazing!',
        'rating': 6  # Invalid rating
    }
    response = test_client.post('/api/books/1/reviews', json=data, headers=auth_headers)
    assert response.status_code == 400

def test_get_book_reviews_no_auth(test_client, create_book, create_review):
    #   Create a book and a review (without auth)
    create_book()
    create_review()

    response = test_client.get('/api/books/1/reviews')
    assert response.status_code == 401

def test_create_review_no_auth(test_client, create_book):
    #   Ensure there's a book to review
    create_book()

    data = {
        'review_text': 'This book was amazing!',
        'rating': 5
    }
    response = test_client.post('/api/books/1/reviews', json=data)
    assert response.status_code == 401