#!/usr/bin/env python3
from unittest import TestCase
from tests import generate_test_env, db, models
from tests.utils import populate

class DatabaseTest(TestCase):
    def setUp(self):
        app, self.ctx, client = generate_test_env()
        # Initialize context for db testing
        self.ctx.push()
        populate(db.session)
    
    def tearDown(self):
        db.session.remove()
        db.drop_all()
        # Close testing context
        self.ctx.pop()
    
    ''' Query sample set from database '''
    def get_sample_set(self):
        user = models.User.query.filter_by(email='test@user.com').first()
        profile = models.Profile.query.filter_by(name='John Doe').first()
        return ( user, profile )

    ''' Ensure server does not persist plain text password and auth interface is cryptographically enforced '''
    def test_user_select(self):
        user, _ = self.get_sample_set()
        assert user.password != 'password'
        assert user.authorize('password')
    
    ''' Check for schema enforced one-to-one relationship '''
    def test_user_profile_relation(self):
        user, profile = self.get_sample_set()
        assert user.profile.id == profile.id