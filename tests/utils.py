from tests import models

''' Populate database with a mock data set '''
def populate(session):
    user = models.User('test@user.com', 'password')
    profile = models.Profile(name="John Doe", user=user)
    session.add(user)
    session.add(profile)
    session.commit()