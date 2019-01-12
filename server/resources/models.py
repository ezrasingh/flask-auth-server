#!/usr/bin/env python3
from server.resources import db
from sqlalchemy.orm import validates, backref
from sqlalchemy.ext.hybrid import hybrid_property, hybrid_method
from flask_security import UserMixin, RoleMixin
from flask_security.utils import hash_password, verify_password
from validate_email import validate_email

roles_users = db.Table(
    'roles_users',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('role_id', db.Integer, db.ForeignKey('role.id'))
)

class Role(RoleMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(256), unique=True, nullable=False)
    password_hash = db.Column(db.String(64), nullable=False)
    active = db.Column(db.Boolean, default=True)
    profile_id = db.Column(db.Integer, db.ForeignKey('profile.id'))
    roles = db.relationship('Role', secondary=roles_users, backref=db.backref('users', lazy='dynamic'))
    
    def __init__(self, email, password, **kwargs):
        self.email = email
        self.password = password

    def __repr__(self):
        return "<User {}:{} profile={}>".format(self.id, self.email, self.profile_id)

    @hybrid_property
    def password(self):
        return self.password_hash
    
    @password.setter
    def password(self, credentials):
        self.password_hash = hash_password(credentials)

    @hybrid_method
    def authorize(self, credentials):
        return verify_password(credentials, self.password_hash)
    
    @validates('email')
    def validate_identity(self, key, address):
        assert validate_email(address)
        return address

class Profile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    user = db.relationship("User", backref='profile', uselist=False)

    def __repr__(self):
        return "<Profile {}:{}>".format(self.id, self.name)
