#!/usr/bin/env python3
import os
from datetime import datetime
from flask import render_template
from flask_emails import Message
from server.resources.utils import Serializer

client = os.getenv('CLIENT_ORIGIN')
mailer = ('Mailer', os.getenv('MAIL_SENDER'))

def send_confirmation_email(email, name):
    context = { 
        'client' : client,
        'confirm_url' : os.getenv('CONFIRMATION_URL'),
        'token' : Serializer.generate_token(email) 
        }
    plain = render_template('emails/user_confirmation.txt', **context)
    msg = Message(
        subject='Welcome, {}'.format(name),
        mail_from=mailer,
        text=plain
    )
    return msg.send(to=email)
    
def send_recovery_email(email):
    context = {
        'client' : client,
        'recover_url' : os.getenv('RECOVER_URL'),
        'token' : Serializer.generate_token(email)
    }
    plain = render_template('emails/account_recovery.txt', **context)
    msg = Message(
        subject='Recover Your Account',
        mail_from=mailer,
        text=plain
    )
    return msg.send(to=email)

def send_startup_email():
    context = { 'time' : datetime.utcnow() }
    plain = render_template('emails/startup.txt', **context)
    msg = Message(
        subject='Auth Server Up',
        mail_from=mailer,
        text=plain
    )
    return msg.send(to=os.getenv('DEVELOPER_EMAIL'))
    