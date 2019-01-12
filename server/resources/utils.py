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