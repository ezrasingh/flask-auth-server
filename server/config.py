#!/usr/bin/env python3
import os

class Config(object):
    DEBUG = False
    TESTING = False
    BCRYPT_LOG_ROUNDS = 15
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class Development(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///db.sqlite3'

class Testing(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'

# For use with Heroku
class Production(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')