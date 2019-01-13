#!/usr/bin/env python3
import os
from server import create_app, config

if 'production' in os.environ:
    app = create_app(mode=config.Production)
else:
    app = create_app(mode=config.Development)

if __name__ == '__main__':
    app.run(debug=True)
