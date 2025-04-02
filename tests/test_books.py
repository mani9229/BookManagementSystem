import json

def test_create_book(test_client, auth_headers):
    data = {
        'title': 'Test Book',
        'author': 'Test Author',
        'genre': 'Fiction'
    }
    response = test_client.post('/api/books', json=data, headers=auth_headers)
    assert response.status_code == 201
    assert response.json['title'] == 'Test Book'

def test_get_books(test_client, auth_headers):
    #   First, create a book
    data = {
        'title': 'Another Book',
        'author': 'Some Author',
        'genre': 'Mystery'
    }
    test_client.post('/api/books', json=data, headers=auth_headers)

    response = test_client.get('/api/books', headers=auth_headers)
    assert response.status_code == 200
    assert len(response.json) > 0

def test_get_book(test_client, auth_headers, create_book):
    #   Create a book first
    create_book(title='Unique Book', author='Special Author', genre='Thriller')
    response = test_client.get('/api/books/1', headers=auth_headers)
    assert response.status_code == 200
    assert response.json['title'] == 'Unique Book'

def test_update_book(test_client, auth_headers, create_book):
    #   Create a book first
    create_book(title='Updatable Book', author='Old Author', genre='Classic')

    updated_data = {'title': 'Updated Title'}
    response = test_client.put('/api/books/1', json=updated_data, headers=auth_headers)
    assert response.status_code == 200
    assert response.json['title'] == 'Updated Title'

def test_delete_book(test_client, auth_headers, create_book):
    #   Create a book first
    create_book(title='Deletable Book', author='Gone Author', genre='Horror')

    response = test_client.delete('/api/books/1', headers=auth_headers)
    assert response.status_code == 200
    assert response.json['message'] == 'Book deleted'
    response_get = test_client.get('/api/books/1', headers=auth_headers)
    assert response_get.status_code == 404

def test_create_book_no_auth(test_client):
    data = {
        'title': 'Unauthorized Book',
        'author': 'Unauthorized Author',
        'genre': 'Unauthorized'
    }
    response = test_client.post('/api/books', json=data)
    assert response.status_code == 401