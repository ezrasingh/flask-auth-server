#!/usr/bin/env python3
import os
from flask import Flask, Blueprint, redirect
from flask_migrate import Migrate
from flask_cors import CORS
from server.resources import db, api, security, user_store
from server.emails import send_startup_email

client = os.getenv('CLIENT_ORIGIN', '*')

migrate = Migrate()
router = Blueprint('api', 'api__module', url_prefix='/api')
cors = CORS(origin=client, headers=[ 'access-control-allow-origin' ])

''' Hooks '''
@router.before_app_first_request
def startup():
    assert send_startup_email().status_code in [ 250 ], 'Failure to start due to Mailer'

''' Generate application instance based on configuration mode '''
def create_app(mode):
    app = Flask(__name__)
    app.config.from_object(mode)
    migrate.init_app(app, db)
    cors.init_app(app)
    api.init_app(router)  
    app.register_blueprint(router)
    with app.app_context():
        security.init_app(app, user_store)
        db.init_app(app)
    return app