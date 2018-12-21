#!/usr/bin/env python3
from server import db, models, config, create_app

app = create_app(mode=config.Testing)