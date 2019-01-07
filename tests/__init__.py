#!/usr/bin/env python3
from server import db, models, config, create_app

''' Return application test instance and context '''
def generate_test_env():
    app = create_app(mode=config.Testing)
    ctx = app.app_context()
    client = app.test_client()
    return ( app, ctx, client )