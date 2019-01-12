#!/usr/bin/env python3
from flask import Flask, Blueprint
from flask_migrate import Migrate
from server.resources import db, api, security, user_store

migrate = Migrate()
router = Blueprint('api', 'router', url_prefix='/api')

''' Generate application instance based on configuration mode '''
def create_app(mode):
    app = Flask(__name__)
    app.config.from_object(mode)
    migrate.init_app(app, db)
    api.init_app(router)
    app.register_blueprint(router)
    with app.app_context():
        security.init_app(app, user_store)
        db.init_app(app)
        db.create_all()
    return app
