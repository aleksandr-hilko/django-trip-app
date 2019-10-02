import pytest
from accounts import views
from django.contrib.auth.models import AnonymousUser
from django.urls import reverse

from .user_factory import UserFactory


@pytest.mark.django_db
def test_user_detail_without_perm(rf):
    """ Verify that client is unable to access GET /api/accounts/<id> if he is not admin or owner """
    user = UserFactory()
    url = reverse("accounts:user", kwargs={'pk': user.id})
    request = rf.get(url)
    request.user = AnonymousUser()
    response = views.UserDetail.as_view()(request)
    assert response.status_code == 403


@pytest.mark.django_db
def test_user_detail_with_own_perm(client):
    """ Verify that owner of account is able to access GET /api/accounts/<id>/ """
    user = UserFactory()
    token_url = reverse("token_obtain_pair")
    resp = client.post(token_url, {'username': user.username, 'password': user.password})
    assert resp.status_code == 200
    user_url = reverse("accounts:user", kwargs={'pk': user.id})
    access_token = resp.json()["access"]
    resp = client.get(user_url, {'Authorization': f'Bearer {access_token}'})
    assert resp.status_code == 200
