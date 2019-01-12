#!/usr/bin/env python3
from server.resources import api, user_store, db, errors
from server.resources.models import Profile
from server.resources.utils import user_is_active, login_required
from flask_restful import Resource, reqparse
from flask_security import current_user
from flask_security.utils import logout_user

@api.resource('/user', endpoint='user')
class User(Resource):
    ''' Initialize endpoint argument parsers '''
    def __init__(self):
        self.parser = {
            'post' : reqparse.RequestParser(trim=True, bundle_errors=True),
            'put' : reqparse.RequestParser(trim=True, bundle_errors=True)
        }
        self.init_parser()

    def init_parser(self):
        # POST parser arguments
        self.parser['post'].add_argument('email', required=True, help='Email is required')
        self.parser['post'].add_argument('password', required=True,help='Password is required')
        self.parser['post'].add_argument('confirm', default=False, help='Confirm the password')
        # PUT parser arguments
        self.parser['put'].add_argument('name', help='User\'s name')

    ''' Request user's profile '''
    @login_required
    @user_is_active
    def get(self):
        user = { 'email' : current_user.email, 'profile' : None }
        if current_user.profile:
            user['profile'] = { 'name' : current_user.profile.name }
        return user

    ''' Create a new user account '''
    def post(self):
        if current_user.is_authenticated:
            return errors.UserAlreadyAuthenticated()
        args = self.parser['post'].parse_args()
        if user_store.find_user(email=args['email']):
            return errors.UserAlreadyExist()
        if args['password'] != args['confirm']:
            return errors.PasswordConfirmationInvalid()
        try:
            user_store.create_user(email=args['email'], password=args['password'])
            db.session.commit()
            # Ensure user must login to new account for first time use
            logout_user()
            return { 'message' : 'Created user' }
        except:
            return errors.UserCreationFailure()

    ''' Update user's profiles '''
    @login_required
    @user_is_active
    def put(self):
        # TODO: Refactor this into a toggle user active flag
        args = self.parser['put'].parse_args()
        if not args:
            return errors.NoUpdatesToMake()
        profile = Profile(user=current_user, **args)
        db.session.commit()
        return { 'message' : 'Profile updated' }

    ''' Deactivate user account '''
    @login_required
    @user_is_active
    def delete(self):
        current_user.active = False
        db.session.commit()
        logout_user()
        return { 'message' : 'Account deactivated' }

