import pytest
from datetime import datetime
from server.resources.models import User
from server.resources import errors

@pytest.mark.incremental
def test_create_user(api, find_user, mock_user):
    ''' Create a new account '''
    res = api.post(
        "/api/user", 
        data=dict(**mock_user, confirm='wrongpass')
    )
    assert res.status_code == 401, "should deny if passswords dont match"
    assert res.json == errors.PasswordConfirmationInvalid, "should prompt error"
    res = api.post(
        "/api/user", 
        data=dict(**mock_user, confirm=mock_user['password'])
    )
    assert res.status_code == 200, "should register if passsword confirmation succeeds"
    assert find_user(**mock_user), "should store user in database"

def test_profile(api, register, mock_user):
    ''' Request user's profile '''
    user = register(**mock_user, confirmed=True)
    assert user, "user should be confirmed"
    headers = { 'Authorization' : user.get_auth_token() }
    res = api.get("/api/user", headers=headers)
    assert res.status_code == 200, "should allow access"
    assert res.json['email'] == mock_user['email'], "account email should match"
    assert res.json['profile']['name'] == mock_user['name'], "account name should match"

def test_update_profile(api, register, mock_user):
    ''' Update user profile '''
    user = register(**mock_user, confirmed=True)
    headers = { 'Authorization' : user.get_auth_token() }
    payload = { 'name' : 'New Name' }
    res = api.put("/api/user", data=payload, headers=headers)
    assert res.status_code == 200, "should allow operation"
    assert res.json['profile']['name'] == 'New Name', "should update profile name"

def test_update_email(api, register, mock_user):
    ''' Update user email with wrong password '''
    user = register(**mock_user, confirmed=True)
    headers = { 'Authorization' : user.get_auth_token() }
    payload = { 'new_email' : 'newemail@mail.com', 'password' : 'wrongpass' }
    res = api.patch("/api/user", data=payload, headers=headers)
    assert res.status_code == 401, "should deny operation"
    assert res.json == errors.InvalidPassword, "should prompt error"
    ''' Update user email '''
    payload['password'] = mock_user['password']
    res = api.patch("/api/user", data=payload, headers=headers)
    assert res.status_code == 200, "should allow operation"
    assert res.json['email'] == 'newemail@mail.com', "should update email"
    ''' Update user email to an existing email '''
    res = api.patch("/api/user", data=payload, headers=headers)
    assert res.status_code == 401, "should deny operation"
    assert res.json == errors.UserAlreadyExist, "should prompt error"

def test_deactivate_user(api, register, mock_user):
    ''' Deactivate user account '''
    user = register(**mock_user, confirmed=True)
    headers = { 'Authorization' : user.get_auth_token() }
    res = api.delete("/api/user", headers=headers)
    assert res.status_code == 200, "should allow access"

    ''' Access resources while deactivated '''
    res = api.get("/api/user", headers=headers)
    assert res.status_code == 401, "should deny access"
    
    ''' Reactivate account '''
    res = api.post("/api/auth", data=mock_user)
    assert res.status_code == 200, "should activate account"
    headers['Authorization'] = res.json['token']
    res = api.get("/api/user", headers=headers)
    assert res.status_code == 200, "should allow access"