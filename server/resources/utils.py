#!/usr/bin/env python3
import os, sys
from itsdangerous import URLSafeTimedSerializer
from flask_restful import abort
from flask_security import current_user
from server.resources import errors, db

''' Check if database is available on network '''
def db_available():
    try:
        session = db.create_scoped_session()
        session.execute('SELECT 1')
        return True, "Database OK!"
    except Exception as e:
        return False, str(e)

''' Decorator to deflect request from deactivated users '''
def user_is_active(f):
    def wrapper(*args, **kwargs):
        if current_user.is_active:
            return f(*args, **kwargs)
        else:
            return errors.AccountNotActive()
    return wrapper

''' REST friendly decorator for enforcing authentication '''
def login_required(f):
    def wrapper(*args, **kwargs):
        if not current_user.is_authenticated:
            return errors.LoginRequired()
        else:
            return f(*args, **kwargs)
    return wrapper

''' Generate authentication tokens for email confirmation process '''
class Serializer():
    serializer = URLSafeTimedSerializer(os.getenv('SECRET_KEY'))

    @staticmethod
    def generate_token(email, **kwargs):
        return Serializer.serializer.dumps(
            email, 
            salt=os.getenv('PASSWORD_SALT')
        )

    @staticmethod
    def confirm_token(token, expiration=3600):
        try:
            email = Serializer.serializer.loads(
                token, 
                salt=os.getenv('PASSWORD_SALT'), 
                max_age=expiration
            )
            return email
        except:
            return False
        
''' Application metadata '''
def app_data():
	return {
        "maintainer": "Ezra Singh",
        "email": "singhezra@gmail.com",
	    "git_repo": "https://github.com/EzraSingh/flask-auth-server",
        "python": sys.version
    }