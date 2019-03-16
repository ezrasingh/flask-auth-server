#!/usr/bin/env python3
import pytest
from server.resources import errors

def test_login_deflection(api, register, mock_user):
    ''' Attempt login of un-registered user '''
    res = api.post("/api/auth", data=mock_user)
    assert res.status_code == 401, "should deny authorization"
    assert res.json == errors.InvalidCredentials, "should prompt error"

    ''' Attempt login of un-confirmed user '''
    user = register(**mock_user)
    res = api.post("/api/auth", data=mock_user)
    assert res.status_code == 400, "should deny authorization"
    assert res.json == errors.UserConfirmationRequired, "should prompt error"

@pytest.mark.incremental
def test_login(api, register, mock_user):
    ''' Attempt login of registered and confirmed user '''
    user = register(**mock_user, confirmed=True)
    res = api.post("/api/auth", data=mock_user)
    assert res.status_code == 200, "should allow authorization"
    assert 'token' in res.json, "should return authorization token"


def test_refresh_token(api, headers, register, mock_user):
    ''' Request token of unauthenticated session '''
    res = api.get("/api/auth", headers=headers)
    assert res.status_code == 401, "should deny request"

    ''' Request new token '''
    user = register(**mock_user, confirmed=True)
    headers['Authorization'] = user.get_auth_token()
    res = api.get("/api/auth", headers=headers)
    assert res.status_code == 200, "should allow refresh"
    assert 'token' in res.json, "should return new token"

def test_recover_account_defelection(api, register, mock_user):
    ''' Request account recovery of non-existing user '''
    res = api.patch("/api/auth", data=mock_user)
    assert res.status_code == 401, "should deny request"
    assert res.json == errors.InvalidCredentials, "should prompt error"

    ''' Request account recovery of existing un-confirmed user '''
    user = register(**mock_user)
    res = api.patch("/api/auth", data=mock_user)
    assert res.status_code == 400, "should deny operation"
    assert res.json == errors.UserConfirmationRequired, "should prompt error"

def test_recover_account(api, register, mock_user):
    ''' Request account recovery of existing confirmed user '''
    user = register(**mock_user, confirmed=True)
    res = api.patch("/api/auth", data=mock_user)
    assert res.status_code == 200, "should allow operation"

def test_reset_password(api, session, register, mock_user):
    ''' Reset user password with wrong password '''
    user = register(**mock_user, confirmed=True)
    headers = { 'Authorization' : user.get_auth_token() }
    payload = { 'password': 'wrongpass', 'new_password': 'newpass', 'confirm': 'newpass' }
    res = api.put("/api/auth", data=payload, headers=headers)
    assert res.status_code == 401, "should deny if password is invalid"
    assert res.json == errors.InvalidCredentials, "should prompt error"
    
    ''' Reset user password with non-matching new passwords '''
    payload.update({ 'password': mock_user['password'], 'confirm': 'wrongpass' })
    res = api.put("/api/auth", data=payload, headers=headers)
    assert res.status_code == 401, "should deny if new passwords do not match"
    assert res.json == errors.PasswordConfirmationInvalid
    
    ''' Reset password '''
    payload['confirm'] = 'newpass'
    res = api.put("/api/auth", data=payload, headers=headers)
    assert res.status_code == 200, "should allow if new passwords match"

def test_delete_account(api, register, mock_user):
    ''' Remove account from user store '''
    user = register(**mock_user, confirmed=True)
    headers = { 'Authorization' : user.get_auth_token() }
    res = api.delete("/api/auth", data=mock_user, headers=headers)
    assert res.status_code == 200, "should process user deletion"
    res = api.post("/api/auth", data=mock_user)
    assert res.status_code == 401, "should confirm user was deleted"