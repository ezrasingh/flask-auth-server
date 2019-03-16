#!/usr/bin/env python3
from sqlalchemy import Table, Column, Integer, String, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import validates, backref, relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.hybrid import hybrid_property, hybrid_method
from flask_security import UserMixin, RoleMixin
from flask_security.utils import hash_password, verify_password
from validate_email import validate_email
from server.resources import db

roles_users = db.Table(
    'roles_users',
    Column('user_id', Integer, ForeignKey('user.id')),
    Column('role_id', Integer, ForeignKey('role.id'))
)

class Role(RoleMixin, db.Model):
    id = Column(Integer, primary_key=True)
    name = Column(String(80), unique=True)
    description = Column(String(255))

class User(UserMixin, db.Model):
    id = Column(Integer, primary_key=True)
    email = Column(String(256), unique=True, nullable=False)
    password_hash = Column(String(64), nullable=False)
    active = Column(Boolean, default=False)
    profile_id = Column(Integer, ForeignKey('profile.id'))
    roles = relationship('Role', secondary=roles_users, backref=backref('users', lazy='dynamic'))
    confirmed_at = Column(DateTime, nullable=True)
    
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
    id = Column(Integer, primary_key=True)
    name = Column(String)
    user = relationship("User", backref='profile', uselist=False)

    def __repr__(self):
        return "<Profile {}:{}>".format(self.id, self.name)
