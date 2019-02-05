#!/usr/bin/env python3
import os
from dotenv import load_dotenv

if not os.getenv('MODE'):
    load_dotenv()

class Config(object):
    DEBUG = False
    TESTING = False
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECURITY_PASSWORD_HASH = 'bcrypt'
    SECRET_KEY = os.getenv('SECRET_KEY')
    SECURITY_PASSWORD_SALT = os.getenv('PASSWORD_SALT')
    SECURITY_TOKEN_AUTHENTICATION_HEADER = 'Authorization'


class Development(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///db.sqlite3'

class Testing(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'

# For use with Docker
class Staging(Config):
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')

# For use with Heroku
class Production(Config):
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')