#!/usr/bin/env python3
import pytest

@pytest.mark.incremental
def test_create_user(test_client, test_user):
    '''
    GIVEN a Flask client
    WHEN '/api/user' endpoint is requested (POST)
    THEN check if user password confirmation is functional 
    '''
    response = test_client.post(
        '/api/user',
        data=dict(**test_user, confirm='wrongpass')
    )
    assert response.status_code == 401
    '''
    GIVEN a Flask client
    WHEN the '/api/user' endpoint is requested (POST)
    THEN check if response is valid
    '''
    response = test_client.post(
        '/api/user', 
        data=dict(**test_user, confirm='letmein')
    )
    assert response.status_code == 200
    assert response.json['message'] == 'Created user'
    '''
    GIVEN a Flask client with an already created account
    WHEN '/api/user' endpoint is requested (POST)
    THEN check if user uniqueness is preserved
    '''
    response = test_client.post(
        '/api/user',
        data=dict(**test_user, confirm='letmein')
    )
    assert response.status_code == 401
    assert response.json['status'] == 401
    assert response.json['message'] == 'A user with that email already exists'
    '''
    GIVEN a Flask client
    WHEN '/api/user' endpoint is requested (PUT)
    THEN check if user is not logged in after creation
    '''
    response = test_client.get('/api/user')
    assert response.status_code == 401

@pytest.mark.incremental
def test_login(test_client, test_user):
    '''
    GIVEN a Flask client
    WHEN a user was created attempt authentication
    THEN check if response is valid
    '''
    response = test_client.post('/api/authenticate', data=test_user)
    assert response.status_code == 200
    assert response.json['message'] == 'Login successful'

def test_profile(test_client, test_user):
    '''
    GIVEN a Flask client
    WHEN '/api/user' endpoint is requested (GET)
    THEN check if profile is accessible
    '''
    response = test_client.get('/api/user')
    assert response.status_code == 200
    assert response.json['email'] == test_user['email']
    assert response.json['profile'] == None

def test_profile_update(test_client, test_user):
    '''
    GIVEN a Flask client
    WHEN '/api/user' endpoint is requested (PUT)
    THEN check if user profile updates were persisted
    '''
    response = test_client.put('/api/user', data=test_user)
    assert response.status_code == 200
    assert response.json['message'] == 'Profile updated'
    response = test_client.get('/api/user')
    assert response.status_code == 200
    assert response.json['email'] == test_user['email']
    assert response.json['profile']['name'] == test_user['name']

@pytest.mark.incremental
def test_deactivate(test_client, test_user):
    '''
    GIVEN a Flask client
    WHEN '/api/user' endpoint is requested (DELETE)
    THEN check if user account is deactivated
    '''
    response = test_client.delete('/api/user')
    assert response.status_code == 200
    assert response.json['message'] == 'Account deactivated'
    response = test_client.get('/api/user')
    assert response.status_code == 401
    response = test_client.put('/api/user', data=test_user)
    assert response.status_code == 401
    response = test_client.post('/api/user', data=test_user)
    assert response.status_code == 401

def test_reactivation(test_client, test_user):
    '''
    GIVEN a Flask client
    WHEN a user logs back in after deactivation
    THEN check if user was reactivated
    '''
    response = test_client.post('/api/authenticate', data=test_user)
    assert response.status_code == 200
    response = test_client.get('/api/user')
    assert response.status_code == 200

def test_logout(test_client, test_user):
    '''
    GIVEN a Flask client
    WHEN '/api/authenticate' endpoint is requested (DELETE)
    THEN check if response is valid
    '''
    response = test_client.delete('/api/authenticate')
    assert response.status_code == 200
    assert response.json['message'] == 'Logout OK'
    response = test_client.get('/api/user')
    assert response.status_code == 401
    assert response.json['message'] == 'Login required'