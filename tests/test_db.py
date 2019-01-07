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
    
    ''' Shutdown context and purge database '''
    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.ctx.pop()
    
    ''' Query sample set from database '''
    def get_sample_set(self):
        user = models.User.query.filter_by(email='test@user.com').first()
        profile = models.Profile.query.filter_by(name='John Doe').first()
        return ( user, profile )

    ''' Ensure users are protected while persisted '''
    def test_user_security(self):
        user, _ = self.get_sample_set()
        # ensure passwords are not stored in plain text
        assert user.password != 'password'
        # ensure passwords are cryptographically enforced
        assert user.authorize('password')
    
    ''' Check for schema enforced one-to-one relationship '''
    def test_user_profile_relation(self):
        user, profile = self.get_sample_set()
        assert user.profile.id == profile.id
    
    ''' Validate that active hybrid property functions correctly '''
    def test_user_active(self):
        user = models.User.query.filter_by(email='test@user.com').first()
        assert user.active
        user.deactivate()
        assert not user.active
        user = models.User.query.filter_by(email='test2@user.com').first()
        assert not user.active