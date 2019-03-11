#!/usr/bin/env python3
import os
from dotenv import load_dotenv

if os.getenv('FLASK_ENV') == 'development':
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
    EMAIL_HOST = os.getenv('EMAIL_HOST')
    EMAIL_PORT = os.getenv('EMAIL_PORT')
    EMAIL_HOST_USER = os.getenv('EMAIL_USERNAME')
    EMAIL_HOST_PASSWORD = os.getenv('EMAIL_PASSWORD')
    EMAIL_TIMEOUT = os.getenv('EMAIL_TIMEOUT')
    EMAIL_USE_SSL = False
    EMAIL_USE_TLS = True


class Development(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///db.sqlite3'
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    EMAIL_SMTP_DEBUG = True

class Testing(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    EMAIL_BACKEND = 'flask_emails.backends.DummyBackend'
    EMAIL_HOST = 'local'
    EMAIL_PORT = 25
    EMAIL_HOST_USER = None
    EMAIL_HOST_PASSWORD = None
    EMAIL_TIMEOUT = 5

# For use with Docker
class Staging(Config):
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')

# For use with Heroku
class Production(Config):
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')