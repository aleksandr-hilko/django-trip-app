import pytest

from accounts.tests.user_factory import faker, UserFactory
from core.constants import User


@pytest.fixture()
def signup_data():
    """ Create signup data for a new user. """
    data = {
        "username": faker.user_name(),
        "password": faker.password(),
        "first_name": faker.first_name(),
        "last_name": faker.last_name(),
        "email": faker.email(),
        "is_staff": False,
        "is_active": True,
    }
    return data


@pytest.fixture
def create_user(signup_data, client):
    """ Create a new user.
        :return: user id, user name and user password.
        """
    password = signup_data.get("password")
    user = User.objects.create_user(**signup_data)
    return user.id, user.username, password


@pytest.fixture
def user():
    """ Create User model in DB. """
    return UserFactory()
