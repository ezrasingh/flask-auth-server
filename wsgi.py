#!/usr/bin/env python3
import os, click
from server import create_app, config
from server.resources.utils import Serializer

try:
    if os.environ['MODE'] == 'production':
        app = create_app(mode=config.Production)
    
    if os.environ['MODE'] == 'staging':
        app = create_app(mode=config.Staging)

except:
    app = create_app(mode=config.Development)

''' CLI Tools '''

''' Generate validation testing for API testing with emails '''
@app.cli.command()
@click.option('--validation-token', default=True, help='Token for confirmation and recovery, for use in API testing')
@click.option('--email', help='Email of user')
def generate(email, **kwargs):
    print("validation_token : ", Serializer.generate_token(email))

if __name__ == '__main__':
    app.run()
