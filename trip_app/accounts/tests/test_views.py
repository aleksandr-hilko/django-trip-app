import pytest
from django.urls import reverse

from .user_factory import UserFactory


@pytest.mark.django_db
class TestUsers:
    def test_user_create(self, client, signup_data):
        """ Verify user is created via GET api/accounts/ """
        url = reverse("accounts:create")
        resp = client.post(url, signup_data)
        assert resp.status_code == 201
        user_dict = resp.json()
        assert user_dict.get("username") == signup_data["username"]
        assert user_dict.get("first_name") == signup_data["first_name"]
        assert user_dict.get("last_name") == signup_data["last_name"]
        assert user_dict.get("email") == signup_data["email"]

    def test_user_list(self, admin_client, user_create_quantity):
        """ Verify that users are displayed with GET api/accounts/ """
        url = reverse("accounts:users")
        resp = admin_client.get(url)
        assert resp.status_code == 200
        # We are increasing expected number by 1 because
        # admin user client is created as well
        assert len(resp.json()) == user_create_quantity + 1

    def test_user_detail(self, admin_client):
        """ Verify that user is returned with GET api/accounts/<user_id>/ """
        user = UserFactory()
        url = reverse("accounts:user", kwargs={"pk": user.id})
        resp = admin_client.get(url)
        assert resp.status_code == 200
        user_dict = resp.json()
        assert user_dict.get("username") == user.username
        assert user_dict.get("first_name") == user.first_name
        assert user_dict.get("last_name") == user.last_name
        assert user_dict.get("email") == user.email

    def test_unauth_user(self, client):
        """ Verify unauthorized user cannot access /api/account/<user_id>/"""
        user = UserFactory()
        url = reverse("accounts:user", kwargs={"pk": user.id})
        resp = client.get(url)
        assert resp.status_code == 403

    def test_user_token_obtain(self, client, create_user):
        """ Verify that existing user is able to obtain a token """
        _, username, password = create_user
        url = reverse("token_obtain_pair")
        resp = client.post(url, {"username": username, "password": password})
        assert resp.status_code == 200
        assert resp.json()["refresh"], "No refresh token provided"
        assert resp.json()["access"], "No access token provided"
