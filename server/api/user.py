#!/usr/bin/env python3
from server.resources import api, user_store, db, errors
from server.resources.utils import user_is_active, login_required
from server.resources.models import Profile
from server.emails import send_confirmation_email
from flask_restful import Resource, reqparse
from flask_security import current_user, auth_token_required
from flask_security.utils import logout_user

@api.resource('/user', endpoint='user')
class User(Resource):
    ''' Initialize endpoint argument parsers '''
    def __init__(self):
        self.parser = {
            'post' : reqparse.RequestParser(bundle_errors=True),
            'put' : reqparse.RequestParser(bundle_errors=True),
            'patch' : reqparse.RequestParser(bundle_errors=True)
        }
        self.init_parser()

    def init_parser(self):
        # POST parser arguments
        self.parser['post'].add_argument('email', trim=True, required=True, help='Email is required')
        self.parser['post'].add_argument('name', trim=True, required=True, help='Name is required')
        self.parser['post'].add_argument('password', required=True,help='Password is required')
        self.parser['post'].add_argument('confirm', required=True, help='Confirm the password')
        # PUT parser arguments
        self.parser['put'].add_argument('name', trim=True, help='User\'s name')
        # PATCH parser arguments
        self.parser['patch'].add_argument('new_email', trim=True, required=True, help='A new email is required')
        self.parser['patch'].add_argument('password', required=True, help='Password is required')

    ''' Request user's profile '''
    @auth_token_required
    @user_is_active
    def get(self):
        user = { 'email' : current_user.email, 'profile' : {} }
        if current_user.profile:
            user['profile'] = { 'name' : current_user.profile.name }
        return user

    ''' Create a new user account '''
    def post(self):
        args = self.parser['post'].parse_args()

        if user_store.find_user(email=args['email']):
            return errors.UserAlreadyExist()
        if args['password'] != args['confirm']:
            return errors.PasswordConfirmationInvalid()

        #try:
        user = user_store.create_user(email=args['email'], password=args['password'])
        profile = Profile(user=user, name=args['name'])
        msg = send_confirmation_email(args['email'], args['name'])
        if msg.status_code not in [ 250 ]:
            return errors.CouldNotSendEmail()
        else:
            db.session.commit()
            logout_user()
            return { 'user' :  user.email  }
        #except Er:
        #    return errors.UserCreationFailure()

    ''' Change user's email '''
    @auth_token_required
    @user_is_active
    def patch(self):
        args = self.parser['patch'].parse_args()

        if user_store.find_user(email=args['new_email']):
            return errors.NoUpdatesToMake()

        if current_user.authorize(args['password']):
            current_user.email = args['new_email']
            db.session.commit()
            return { 'email': current_user.email }
        else:
            return errors.InvalidCredentials()

    ''' Update user's profile '''
    @auth_token_required
    @user_is_active
    def put(self):
        args = self.parser['put'].parse_args()
        if not args:
            return errors.NoUpdatesToMake()
        profile = Profile(user=current_user, **args)
        db.session.commit()
        return { 'profile' : { 'name' : profile.name } }

    ''' Deactivate user account '''
    @auth_token_required
    @user_is_active
    def delete(self):
        user_store.deactivate_user(current_user)
        db.session.commit()
        logout_user()
        return { 'message' : 'Account deactivated' }

