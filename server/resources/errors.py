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

NoUpdatesToMake = ApiError(401, 'No updates made')

UserCreationFailure = ApiError(500, 'Could not create user')
