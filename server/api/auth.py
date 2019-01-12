#!/usr/bin/env python3
from server.resources import api, user_store, db, errors
from server.resources.utils import login_required
from flask_restful import Resource, reqparse
from flask_security import current_user
from flask_security.utils import login_user, logout_user

'''  Login with identity and credentials '''
def login(email, password, remember=False):
    user = user_store.find_user(email=email)
    if user is None or not user.authorize(password):
        return errors.InvalidCredentials()
    # If user issues new login after deactivation, reactivate their account
    elif not user.active:
        user.active = True
        db.session.commit()
    login_user(user, remember=remember)
    return { 'message' : 'Login successful' }

@api.resource('/authenticate', endpoint='auth')
class Authentication(Resource):
    ''' Initialize endpoint argument parsers '''
    def __init__(self):
        self.parser = {
            'post' : reqparse.RequestParser(bundle_errors=True)
        }
        self.init_parser()

    def init_parser(self):
        # POST parser arguments
        self.parser['post'].add_argument('email', required=True, help='Email is required')
        self.parser['post'].add_argument('password', required=True, help='Password is required')
        self.parser['post'].add_argument('remember', type=bool)

    ''' Establish user session '''
    def post(self):
        if current_user.is_authenticated:
            return errors.UserAlreadyAuthenticated()
        args = self.parser['post'].parse_args()
        return login(**args)
        

    @login_required
    def delete(self):
        logout_user()
        return { 'message': 'Logout OK' }
        