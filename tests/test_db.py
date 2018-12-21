#!/usr/bin/env python3
import unittest
from tests import app, db

class DatabaseTest(unittest.TestCase):
    def setUp(self):
        with app.app_context():
            self.populate()
    
    def tearDown(self):
        # NOTE - Testing config uses in-memory SQLite which is volatile by design
        with app.app_context():
            db.session.remove()
    
    def populate(self):
        pass