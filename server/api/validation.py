#!/usr/bin/env python3
from datetime import datetime
from server.resources import api, user_store, db, errors
from server.resources.utils import Serializer
from server.emails import send_confirmation_email
from flask_restful import Resource, reqparse

def user_confirmation(token, **kwargs):
    email = Serializer.confirm_token(token)
    user = user_store.find_user(email=email)
    if user:
        user_store.activate_user(user)
        user.confirmed_at = datetime.utcnow()
        db.session.commit()
        return { 'message' : 'Account confirmed' }
    else:
        return errors.InvalidToken()

def password_reset(token, new_password, confirm, **kwargs):
    email = Serializer.confirm_token(token)
    user = user_store.find_user(email=email)
    if user:
        if new_password == confirm:
            user.password = new_password
            db.session.commit()
            return { 'message' : 'Password reset' }
        else:
            return errors.PasswordConfirmationInvalid()
    else:
        return errors.InvalidToken()

def resend_user_confirmation(email, **kwargs):
    user = user_store.find_user(email=email)
    if not user.confirmed_at:
        msg = send_confirmation_email(email, name=user.profile.name)
        if msg.status_code not in [ 250 ]:
            return errors.CouldNotSendEmail()
        else:
            return { 'message' : 'New confirmation link sent' }
    else:
        return errors.UserAlreadyConfirmed()

@api.resource('/validate/<action>', endpoint='validate')
class Validation(Resource):
    def __init__(self):
        self.parser = {
            'post' : reqparse.RequestParser(bundle_errors=True),
            'put' : reqparse.RequestParser(bundle_errors=True)
        }
        self.init_parser()

    def init_parser(self):
        # POST arguments
        self.parser['post'].add_argument('token', required=True, help='Validation token required')
        self.parser['post'].add_argument('new_password')
        self.parser['post'].add_argument('confirm')
        # PUT arguments
        self.parser['put'].add_argument('email')

    ''' Validation interface '''
    def post(self, action):
        args = self.parser['post'].parse_args()
        if 'confirm' == action:
            return user_confirmation(**args)
        if 'reset' == action:
            if not args['new_password']:
                return errors.NoUpdatesToMake()
            return password_reset(**args)
        else:
            return errors.MissingValidatorAction()
    
    ''' Re-Validation interface '''
    def put(self, action):
        args = self.parser['put'].parse_args()
        if 'confirm' == action:
            if not args['email']:
                return errors.NoUpdatesToMake()
            return resend_user_confirmation(**args)
        else:
            return errors.MissingValidatorAction()
