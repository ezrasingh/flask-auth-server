#!/usr/bin/env python3
from server.resources import api, user_store, db, errors
from server.resources.utils import user_is_active
from flask_restful import Resource, reqparse
from flask_security import current_user, auth_token_required
from flask_security.utils import login_user, logout_user
from server.emails import send_recovery_email

'''  Login with identity and credentials '''
def login(email, password, remember=False):
    user = user_store.find_user(email=email)
    if user is None or not user.authorize(password):
        return errors.InvalidCredentials()
    if not user.confirmed_at:
            return errors.UserConfirmationRequired()
    # If user issues new login after deactivation, reactivate their account
    if not user.active:
        user.active = True
        db.session.commit()
    login_user(user, remember=remember)
    return { 'token' : user.get_auth_token() }

@api.resource('/auth', endpoint='auth')
class Authentication(Resource):
    ''' Initialize endpoint argument parsers '''
    def __init__(self):
        self.parser = {
            'post' : reqparse.RequestParser(bundle_errors=True),
            'put' : reqparse.RequestParser(bundle_errors=True),
            'delete' : reqparse.RequestParser(bundle_errors=True),
            'patch': reqparse.RequestParser(bundle_errors=True)
        }
        self.init_parser()

    def init_parser(self):
        # POST parser arguments
        self.parser['post'].add_argument('email', trim=True, required=True, help='Email is required')
        self.parser['post'].add_argument('password', required=True, help='Password is required')
        self.parser['post'].add_argument('remember', type=bool)
        # PUT parser arguments
        self.parser['put'].add_argument('password', required=True, help='Current password is required')
        self.parser['put'].add_argument('new_password', required=True, help='New password is required')
        self.parser['put'].add_argument('confirm', required=True, help='Please confirm new password')
        # DELETE parser arguments
        self.parser['delete'].add_argument('password', required=True, help='Password is required')
        # PATCH arguments
        self.parser['patch'].add_argument('email', trim=True, required=True)

    ''' Refresh auth token '''
    @auth_token_required
    def get(self):
        return { 'token' : current_user.get_auth_token() }

    ''' Login user '''
    def post(self):
        args = self.parser['post'].parse_args()
        return login(**args)
    
    ''' Reset password '''
    @auth_token_required
    def put(self):
        args = self.parser['put'].parse_args()
        if args['new_password'] != args['confirm']:
            return errors.PasswordConfirmationInvalid()

        if current_user.authorize(args['password']):
            current_user.password = args['new_password']
            db.session.commit()
            return { 'message' : 'Password updated' }
        else:
            return errors.InvalidCredentials()
    
    ''' Recover account '''
    def patch(self):
        args = self.parser['patch'].parse_args()
        if user_store.find_user(email=args['email']):
            msg = send_recovery_email(args['email'])
            if msg.status_code in [ 250 ]:
                return { 'message': 'Recovery link sent' }
            else:
                return errors.CouldNotSendEmail()
        else:
            return errors.InvalidCredentials()

    ''' Remove account '''
    @auth_token_required
    @user_is_active
    def delete(self):
        args = self.parser['delete'].parse_args()
        if current_user.authorize(args['password']):
            user_store.delete_user(current_user)
            db.session.commit()
            logout_user()
            return { 'Message' : 'Account removed' }
        else:
            return errors.InvalidCredentials()        