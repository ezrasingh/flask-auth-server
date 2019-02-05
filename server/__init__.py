#!/usr/bin/env python3
import os
from flask import Flask, Blueprint
from flask_migrate import Migrate
from flask_cors import CORS
from server.resources import db, api, security, user_store

migrate = Migrate()
router = Blueprint('api', 'router', url_prefix='/api')
cors = CORS(origin=os.getenv('CLIENT_ORIGIN'), headers=[ 'access-control-allow-origin' ])

''' Generate application instance based on configuration mode '''
def create_app(mode):
    app = Flask(__name__)
    app.config.from_object(mode)
    migrate.init_app(app, db)
    api.init_app(router)
    cors.init_app(app)
    app.register_blueprint(router)
    with app.app_context():
        security.init_app(app, user_store)
        db.init_app(app)
        db.create_all()
    return app
