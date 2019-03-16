#!/usr/bin/env python3
import pytest
from server.resources.models import User, Profile

@pytest.mark.incremental
def test_user_model(db, session, mock_user):
    '''
    GIVEN a SQLAlchemy model
    WHEN a user is created
    THEN check if credentials are cryptographically enforced
    '''
    user = User(**mock_user)
    assert user.email == mock_user['email'], 'Email was not set'
    assert user.password != mock_user['password'], 'Password was stored in plaintext'
    assert user.authorize(mock_user['password']), 'User authorization scheme failed'
    db.session.commit()

def test_profile_model(session, mock_user):
    '''
    GIVEN a SQLAlchemy model
    WHEN a profile is created
    THEN check one-to-one relationship between user and profile
    '''
    user = User(**mock_user)
    profile = Profile(name=mock_user['name'], user=user)
    assert user.profile.id == profile.id, 'One-to-One User-Profile assignment failed'
    session.commit()