import pytest
from accounts.tests.user_factory import faker
from django.contrib.auth import get_user_model

User = get_user_model()


@pytest.fixture
def signup_data():
    data = {
        'username': faker.user_name(),
        'password': faker.password(),
        'first_name': faker.first_name(),
        'last_name': faker.last_name(),
        'email': faker.email(),
        'is_staff': False,
        'is_active': False
    }
    return data


@pytest.fixture
def create_user(signup_data, client):
    """" Create a new user and return user id, username and user password """
    password = signup_data.pop('password')
    user = User.objects.create_user(username=signup_data["username"], password=password)
    return user.id, user.username, password
