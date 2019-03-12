#!/usr/bin/env python3
import pytest
from server.resources import errors
from server.resources.utils import Serializer

def test_confirm_user_registration(api, register, mock_user):
    ''' Confirm a newly registered user '''
    user = register(**mock_user)
    payload = { 'token' : 'badtoken' }
    res = api.post("/api/validate/confirmation", data=payload)
    assert res.status_code == 400, "should deny operation if token is invalid"
    assert res.json == errors.InvalidToken, "should prompt error"
    payload['token'] = Serializer.generate_token(**mock_user)
    res = api.post("/api/validate/confirmation", data=payload)
    assert res.status_code == 200, "should allow operation if token is valid"

def test_resend_confirmation_defelection(api, register, mock_user):
    ''' Resend user confirmation link of non-existing user '''
    payload = { 'email' : 'wrongemail' }
    res = api.put("/api/validate/confirmation", data=payload)
    assert res.status_code == 401, "should deny operation"
    assert res.json == errors.InvalidCredentials, "should prompt error"
    
    ''' Resend user confirmation link of already confirmed user '''
    user = register(**mock_user, confirmed=True)
    payload['email'] = user.email
    res = api.put("/api/validate/confirmation", data=payload)
    assert res.status_code == 401, "should deny operation"
    assert res.json == errors.UserAlreadyConfirmed, "should prompt error"

def test_resend_confirmation(api, register, mock_user):
    ''' Resend user confirmation link '''
    user = register(**mock_user)
    payload = { 'email' : user.email }
    res = api.put("/api/validate/confirmation", data=payload)
    assert res.status_code == 200, "should allow operation"

def test_validate_account_recovery(api, register, mock_user):
    ''' Recover account with invalid token '''
    user = register(**mock_user, confirmed=True)
    payload = { 'token' : 'badtoken', 'new_password' : 'newpass', 'confirm' : 'newpass' }
    res = api.post("/api/validate/recovery", data=payload)
    assert res.status_code == 400, "should deny operation if token is invalid"
    assert res.json == errors.InvalidToken, "should prompt error"
    
    ''' Recover account with non-matching new passwords '''
    payload['token'] = Serializer.generate_token(**mock_user)
    payload['confirm'] = 'wrongpass'
    res = api.post("/api/validate/recovery", data=payload)
    assert res.status_code == 401, "should deny if new passwords do not match"
    assert res.json == errors.PasswordConfirmationInvalid, "should prompt error"
    ''' Reset password and recover account '''
    payload['confirm'] = 'newpass'
    res = api.post("/api/validate/recovery", data=payload)
    assert res