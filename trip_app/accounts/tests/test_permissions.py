import pytest
from django.urls import reverse

from .user_factory import UserFactory
from django.contrib.auth import get_user_model

User = get_user_model()


@pytest.mark.django_db
def test_user_detail_without_perm(client):
    """ Verify that client is unable to access GET /api/accounts/<id>
        if he is not admin or owner. """
    user = UserFactory()
    url = reverse("accounts:user", kwargs={"pk": user.id})
    response = client.get(url)
    assert response.status_code == 403


@pytest.mark.django_db
def test_user_detail_with_own_perm(client, create_user):
    """ Verify that owner of account is able to access
        GET /api/accounts/<id>/. """
    id_, username, password = create_user
    client.login(username=username, password=password)
    token_url = reverse("token_obtain_pair")
    resp = client.post(token_url, {"username": username, "password": password})
    assert resp.status_code == 200
    user_url = reverse("accounts:user", kwargs={"pk": id_})
    access_token = resp.json()["access"]
    resp = client.get(user_url, {"Authorization": f"Bearer {access_token}"})
    assert resp.status_code == 200
    assert resp.json().get("username") == username
