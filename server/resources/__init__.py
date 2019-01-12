#!/usr/bin/env python3
from flask_sqlalchemy import SQLAlchemy
from flask_security import Security, SQLAlchemyUserDatastore
from flask_restful import Api

''' Application resources '''
db = SQLAlchemy()
security = Security()
api = Api()

''' User store '''
import server.resources.models as models

user_store = SQLAlchemyUserDatastore(db, models.User, models.Role)

''' Api endpoints '''
from server.api.auth import Authentication
from server.api.user import User