#!/usr/bin/env python3
from datetime import datetime
from server.resources import api, user_store, db, errors
from server.resources.utils import Serializer
from server.emails import send_confirmation_email
from flask_restful import Resource, reqparse

@api.resource('/validate/confirmation', endpoint='account_confirmation')
class ConfirmationValidation(Resource):
    def __init__(self):
        self.parser = {
            'post' : reqparse.RequestParser(bundle_errors=True),
            'put' : reqparse.RequestParser(bundle_errors=True)
        }
        self.init_parser()

    def init_parser(self):
        # POST arguments
        self.parser['post'].add_argument('token', required=True, help='Validation token required')
        # PUT arguments
        self.parser['put'].add_argument('email', required=True, help='Please enter your email address')

    ''' Confirm user registration '''
    def post(self):
        args = self.parser['post'].parse_args()
        email = Serializer.confirm_token(args['token'])
        if not email:
            return errors.InvalidToken()
        user = user_store.find_user(email=email)
        if user:
            user_store.activate_user(user)
            user.confirmed_at = datetime.utcnow()
            db.session.commit()
            return { 'message' : 'Account confirmed' }
        else:
            return errors.InvalidToken()
    
    ''' Resend confirmation link '''
    def put(self):
        args = self.parser['put'].parse_args()
        user = user_store.find_user(email=args['email'])
        if not user:
            return errors.InvalidCredentials()
        if not user.confirmed_at:
            msg = send_confirmation_email(user.email, name=user.profile.name)
            if msg.status_code not in [ 250 ]:
                return errors.CouldNotSendEmail()
            else:
                return { 'message' : 'New confirmation link sent' }
        else:
            return errors.UserAlreadyConfirmed()

@api.resource('/validate/recovery', endpoint='account_recovery')
class RecoveryValidation(Resource):
    def __init__(self):
        self.parser = { 'post' : reqparse.RequestParser(bundle_errors=True) }
        self.init_parser()
    
    def init_parser(self):
        # POST arguments
        self.parser['post'].add_argument('token', required=True, help='Validation token required')
        self.parser['post'].add_argument('new_password', required=True, help='Please set a new password')
        self.parser['post'].add_argument('confirm', required=True, help='New password confirmation required')

    ''' Reset password, account recovery '''
    def post(self):
        args = self.parser['post'].parse_args()
        email = Serializer.confirm_token(args['token'])
        if not email:
            return errors.InvalidToken()
        user = user_store.find_user(email=email)
        if user:
            if args['new_password'] == args['confirm']:
                user.password = args['new_password']
                db.session.commit()
                return { 'message' : 'Password reset' }
            else:
                return errors.PasswordConfirmationInvalid()
        else:
            return errors.InvalidToken()