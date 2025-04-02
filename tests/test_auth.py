import json

def test_register(test_client):
    data = {
        'username': 'newuser',
        'password': 'newpassword'
    }
    response = test_client.post('/api/register', json=data)
    assert response.status_code == 201
    assert response.json['username'] == 'newuser'

def test_register_duplicate_user(test_client):
    #   Register a user first
    data = {
        'username': 'duplicateuser',
        'password': 'somepassword'
    }
    test_client.post('/api/register', json=data)

    #   Try to register again with the same username
    response = test_client.post('/api/register', json=data)
    assert response.status_code == 400
    assert response.json['message'] == 'Username already exists'

def test_login(test_client):
    #   Register a user first
    test_client.post('/api/register', json={'username': 'loginuser', 'password': 'loginpassword'})

    data = {
        'username': 'loginuser',
        'password': 'loginpassword'
    }
    response = test_client.post('/api/login', json=data)
    assert response.status_code == 200
    assert 'access_token' in response.json

def test_login_invalid_credentials(test_client):
    #   Register a user first
    test_client.post('/api/register', json={'username': 'baduser', 'password': 'badpassword'})

    data = {
        'username': 'baduser',
        'password': 'wrongpassword'
    }
    response = test_client.post('/api/login', json=data)
    assert response.status_code == 401
    assert response.json['message'] == 'Invalid credentials'