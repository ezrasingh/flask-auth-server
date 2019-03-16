import pytest
from datetime import datetime
from server import create_app, config
from server.resources import db as _db
from server.resources.models import User, Profile
from server.resources.utils import Serializer

''' Session-wide test application. '''
@pytest.yield_fixture(scope='session')
def app(request):
    app = create_app(mode=config.Testing)
    with app.app_context():
        yield app

'''  Session-wide test client '''
@pytest.yield_fixture(scope='session')
def api(app):
    with app.app_context():
        _db.create_all()
        _db.app = app
        with app.test_client() as client:
            yield client
        _db.drop_all()

''' Session-wide test Database '''
@pytest.yield_fixture(scope='session')
def db(app, request):
    with app.app_context():
        _db.app = app
        _db.create_all()
        def teardown():
           _db.drop_all()
        request.addfinalizer(teardown)
        yield _db

''' New database session for a test '''
@pytest.yield_fixture(scope='function')
def session(app, db, request):
    # reset db each session for consistent testing conditions
    _db.drop_all()
    _db.create_all()
    with app.app_context():
        connection = _db.engine.connect()
        transaction = connection.begin()
        options = dict(bind=connection, binds={})
        session = db.create_scoped_session(options=options)
        def teardown():
            session.rollback()
            session.close()
            connection.close()
            session.remove()
        request.addfinalizer(teardown)
        yield session


''' Helper Fixtures '''

''' Find and return an existing user '''
@pytest.fixture(scope='function')
def find_user(session):
   def get_user(email, **kwargs):
        user = session.query(User).filter_by(email=email).first()
        assert user, "user does not exist"
        return user
   return get_user

''' Register new user directly to the database '''
@pytest.yield_fixture(scope='function')
def register(session):
    def create_user(email, password, name, confirmed=False):
        user = User(email, password)
        assert user, "user creation failed"
        profile = Profile(name=name, user=user)
        assert profile, "profile creation failed"
        if confirmed:
            user.active = True
            user.confirmed_at = datetime.utcnow()
        session.add(user)
        session.add(profile)
        session.commit()
        return user
    return create_user

''' Mock Fixtures '''

@pytest.fixture
def headers():
    return { 'Authorization' : None }

@pytest.fixture
def mock_user():
    return dict(email='tester@email.com', password='letmein', name='John Doe')
