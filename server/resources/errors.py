#!/usr/bin/env python3

''' Wrapper for returning REST friendly error messages '''
class ApiError(dict):
    def __init__(self, status, message):
        self.update({ 'status' : status, 'message' : message })
    
    def __call__(self):
        return self, self['status']

LoginRequired = ApiError(401, 'Login required')

UserAlreadyAuthenticated = ApiError(401, 'You are already logged in')

UserAlreadyExist = ApiError(401, 'A user with that email already exists')

InvalidCredentials = ApiError(401, 'Invalid email or password')

PasswordConfirmationInvalid = ApiError(401, 'Passwords do not match')

AccountNotActive = ApiError(401, 'User account not active')

NoUpdatesToMake = ApiError(401, 'No updates to make')

UserCreationFailure = ApiError(500, 'Could not create user')

CouldNotSendEmail = ApiError(500, 'Server could not process email request')

UserConfirmationRequired = ApiError(400, 'Please confirm your account')

MissingValidatorAction = ApiError(500, 'Missing validator action type')

InvalidToken = ApiError(400, 'Invalid validation token')

AccountNotActive = ApiError(401, 'Account is deactivated login to reactivate')

UserAlreadyConfirmed = ApiError(401, 'Account already confirmed')

InvalidPassword = ApiError(401, 'Password is incorrect')