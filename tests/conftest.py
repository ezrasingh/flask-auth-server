#!/usr/bin/env python3
import pytest, os
from server import create_app, config
from server.resources import db

if os.getenv('MODE') == 'staging':
    app = create_app(mode=config.Staging)
else:
    app = create_app(mode=config.Testing)

@pytest.fixture(scope='module')
def test_user():
    return {
            'email' : 'tester@user.com',
            'password' : 'letmein',
            'name' : 'John Doe'
    }

''' A flask client with a user already authenticated '''
@pytest.fixture(scope='session')
def test_client():
    with app.app_context():
        db.create_all()
        yield app.test_client()
        db.session.remove()
        db.drop_all()
