#!/usr/bin/env python3
import pytest
from server.resources.models import User, Profile

@pytest.mark.incremental
def test_user_model(test_user):
    '''
    GIVEN a SQLAlchemy model
    WHEN a user is created
    THEN check if credentials are cryptographically enforced
    '''
    user = User(**test_user)
    assert user.email == test_user['email'], 'Email was not set'
    assert user.password != test_user['password'], 'Password was stored in plaintext'
    assert user.authorize(test_user['password']), 'User authorization scheme failed'

def test_profile_model(test_user):
    '''
    GIVEN a SQLAlchemy model
    WHEN a profile is created
    THEN check one-to-one relationship between user and profile
    '''
    user = User.query.filter_by(email=test_user['email']).first()
    profile = Profile(name=test_user['name'], user=user)
    assert user.profile.id == profile.id, 'One-to-One User-Profile assignment failed'
