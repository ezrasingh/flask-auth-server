#!/usr/bin/env python3
import os
from server import create_app, config

if os.environ['MODE'] == 'production':
    app = create_app(mode=config.Production)

if os.environ['MODE'] == 'staging':
    app = create_app(mode=config.Staging)

else:
    app = create_app(mode=config.Development)

if __name__ == '__main__':
    app.run()
