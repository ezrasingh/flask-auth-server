#!/usr/bin/env python3
import os
from itsdangerous import URLSafeTimedSerializer
from flask_restful import abort
from flask_security import current_user
from server.resources import errors

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