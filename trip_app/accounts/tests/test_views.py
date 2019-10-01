import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse

from .user_factory import UserFactory

User = get_user_model()


@pytest.fixture
def signup_data():
    data = {
        'username': 'test',
        'password': 'foo',
        'first_name': 'test',
        'last_name': 'test',
        'email': 'test@yahoo.com',
        'is_staff': False,
        'is_active': False
    }
    return data


@pytest.mark.django_db
class TestUsers:
    def test_user_create(self, client, signup_data):
        """ Verify user is created via GET api/accounts/ """
        url = reverse("accounts:users")
        resp = client.post(url, signup_data)
        assert resp.status_code == 201
        user_dict = resp.json()
        print(user_dict)
        assert user_dict.get('username') == signup_data['username']
        assert user_dict.get('first_name') == signup_data['first_name']
        assert user_dict.get('last_name') == signup_data['last_name']
        assert user_dict.get('email') == signup_data['email']

    @pytest.mark.parametrize('user_qty', [0, 1, 10, 100])
    def test_list(self, client, user_qty):
        """ Verify that users are displayed with GET api/accounts/ """
        UserFactory.create_batch(size=user_qty, is_staff=False)
        url = reverse("accounts:users")
        resp = client.get(url)
        assert resp.status_code == 200
        assert len(resp.json()) == user_qty

    def test_unauth_user(self, client):
        """ Verify unauthorized user cannot access /api/account/{id}/"""
        user = UserFactory()
        url = reverse("accounts:user", kwargs={'pk': user.id})
        resp = client.get(url)
        assert resp.status_code == 403

    def test_with_authenticated_client(self, client):
        user = UserFactory(password="foo")
        url = reverse("token_obtain_pair")
        print({'username': user.username, 'password': user.password})
        resp = client.post(url, {'username': user.username, 'password': user.password})
        print(resp.status_code)
        assert resp.content == 200
