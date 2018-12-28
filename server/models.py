#!/usr/bin/env python3
from server import db, crypto
from sqlalchemy.orm import validates, backref
from sqlalchemy.ext.hybrid import hybrid_property, hybrid_method
from validate_email import validate_email

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(256), unique=True, nullable=False)
    secret = db.Column(db.LargeBinary(64), nullable=False)
    profile_id = db.Column(db.Integer, db.ForeignKey('profile.id'))
    
    ''' Adapter for reading/writing user's secret '''
    @hybrid_property
    def password(self):
        return self.secret

    @password.setter
    def password(self, credentials):
        self.secret = crypto.generate_password_hash(credentials)

    @hybrid_method
    def authorize(self, credentials):
        return crypto.check_password_hash(self.secret, credentials)
    
    @validates('email')
    def validate_identity(self, key, address):
        assert validate_email(address)
        return address
    
    def __init__(self, email, password):
        self.email = email
        self.password = password

    def __repr__(self):
        return "<User {}:{}>".format(self.id, self.email)

class Profile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    user = db.relationship("User", backref='profile', uselist=False)

    def __repr__(self):
        return "<Profile {}:{}>".format(self.id, self.name)