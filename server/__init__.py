#!/usr/bin/env python3
import os
from flask import Flask, Blueprint
from flask_migrate import Migrate
from flask_cors import CORS
from healthcheck import HealthCheck, EnvironmentDump
from server.resources import api, db, security, user_store
from server.resources.utils import db_available, app_data
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
    attach_monitor(app)
    api.init_app(router)  
    app.register_blueprint(router)
    with app.app_context():
        db.init_app(app)
        db.create_all()
        security.init_app(app, user_store)
    return app

''' Attach status and environment endpoints for monitoring server health '''
def attach_monitor(app):
    health = HealthCheck(app, '/status')
    envdump = EnvironmentDump(
        app,
        '/env',
        include_os=False, include_config=False,
        include_process=False, include_python=False
        )

    health.add_check(db_available)
    envdump.add_section("application", app_data)