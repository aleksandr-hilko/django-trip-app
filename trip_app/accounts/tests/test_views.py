import pytest
from core.utils import raise_for_status
from django.urls import reverse

from .user_factory import UserFactory, faker


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
def create_user_dict(signup_data, client):
    """" Create a new user via POST /api/accounts/.
         Exception will be raised in case of bas response """
    url = reverse("accounts:create")
    resp = client.post(url, signup_data)
    raise_for_status(resp)
    print(f"user created {resp.json()}")
    return signup_data


@pytest.mark.django_db
class TestUsers:
    def test_user_create(self, client, signup_data):
        """ Verify user is created via GET api/accounts/ """
        url = reverse("accounts:create")
        resp = client.post(url, signup_data)
        assert resp.status_code == 201
        user_dict = resp.json()
        print(user_dict)
        assert user_dict.get('username') == signup_data['username']
        assert user_dict.get('first_name') == signup_data['first_name']
        assert user_dict.get('last_name') == signup_data['last_name']
        assert user_dict.get('email') == signup_data['email']

    @pytest.mark.parametrize('user_qty', [0, 1, 10, 100])
    def test_user_list(self, admin_client, user_qty):
        """ Verify that users are displayed with GET api/accounts/ """
        UserFactory.create_batch(size=user_qty, is_staff=False, )
        url = reverse("accounts:users")
        resp = admin_client.get(url)
        assert resp.status_code == 200
        # We are increasing expected number by 1 because admin user client is created as well
        assert len(resp.json()) == user_qty + 1

    def test_user_detail(self, admin_client):
        """ Verify that user is returned with GET api/accounts/<user_id>/ """
        user = UserFactory()
        url = reverse("accounts:user", kwargs={'pk': user.id})
        resp = admin_client.get(url)
        assert resp.status_code == 200
        user_dict = resp.json()
        assert user_dict.get('username') == user.username
        assert user_dict.get('first_name') == user.first_name
        assert user_dict.get('last_name') == user.last_name
        assert user_dict.get('email') == user.email

    def test_unauth_user(self, client):
        """ Verify unauthorized user cannot access /api/account/<user_id>/"""
        user = UserFactory()
        url = reverse("accounts:user", kwargs={'pk': user.id})
        resp = client.get(url)
        assert resp.status_code == 403

    def test_user_token_obtain(self, client, create_user_dict):
        """ Verify that existing user is able to obtain a token """
        url = reverse("token_obtain_pair")
        resp = client.post(url, {'username': create_user_dict['username'], 'password': create_user_dict['password']})
        print(resp.status_code)
        assert resp.status_code == 200
