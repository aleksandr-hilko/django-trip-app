import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse

from trips.tests.trip_factory import TripFactory, TripRequestFactory

User = get_user_model()


@pytest.mark.django_db
def test_unable_update(client, create_user):
    """ Verify that authenticated non driver, non admin can't update
        trip with PATCH api/trips/<trip_id>/. """
    _, username, password = create_user
    client.login(username=username, password=password)
    trip = TripFactory()
    url = reverse("trips-detail", args=[trip.id])
    resp = client.patch(url, {"price": 20}, content_type="application/json")
    assert resp.status_code == 403


@pytest.mark.django_db
def test_unable_delete(client, create_user):
    """ Verify that authenticated non driver, non admin can't delete
        trip with DELETE api/trips/<trip_id>/.  """
    _, username, password = create_user
    client.login(username=username, password=password)
    trip = TripFactory()
    url = reverse("trips-detail", args=[trip.id])
    resp = client.delete(url)
    assert resp.status_code == 403


@pytest.mark.django_db
def test_driver_delete(client, create_user):
    """ Verify that driver can delete it's own trip with
        DELETE api/trips/<trip_id>/. """
    pk, username, password = create_user
    user = User.objects.get(pk=pk)
    trip = TripFactory(driver=user)
    client.login(username=username, password=password)
    url = reverse("trips-detail", args=[trip.id])
    resp = client.delete(url)
    assert resp.status_code == 204


@pytest.mark.django_db
def test_driver_update(client, create_user):
    """ Verify that driver can delete it's own trip
        with PATCH api/trips/<trip_id>/. """
    pk, username, password = create_user
    user = User.objects.get(pk=pk)
    trip = TripFactory(driver=user)
    client.login(username=username, password=password)
    url = reverse("trips-detail", args=[trip.id])
    resp = client.patch(url, {"price": 20.00}, content_type="application/json")
    assert resp.status_code == 200
    assert float(resp.json()["price"]) == 20.00


@pytest.mark.django_db
def test_admin_delete(admin_client):
    """ Verify that admin can delete trip with DELETE api/trips/<trip_id>/. """
    trip = TripFactory()
    url = reverse("trips-detail", args=[trip.id])
    resp = admin_client.delete(url)
    assert resp.status_code == 204


@pytest.mark.django_db
@pytest.mark.parametrize(
    "url", ["trip-requests-approve", "trip-requests-decline"]
)
def test_user_unable_approve_decline(client, create_user, url):
    """ Verify that authenticated non driver, non admin can't approve(decline)
        trip request with POST api/trip-requests/<id>/approve(decline). """
    _, username, password = create_user
    client.login(username=username, password=password)
    trip_request = TripRequestFactory()
    request_url = reverse(url, args=[trip_request.id])
    resp = client.post(request_url)
    assert resp.status_code == 403


@pytest.mark.django_db
@pytest.mark.parametrize(
    "url, status",
    [
        ("trip-requests-approve", "Approved"),
        ("trip-requests-decline", "Declined"),
    ],
)
def test_owner_approve_decline(client, create_user, url, status):
    """ Verify that driver can approve(decline) trip request with
        POST api/trip-requests/<id>/approve(decline). """
    _, username, password = create_user
    user = User.objects.get(username=username)
    client.login(username=username, password=password)
    trip = TripFactory(driver=user)
    trip_request = TripRequestFactory(trip=trip)
    request_url = reverse(url, args=[trip_request.id])
    resp = client.post(request_url)
    assert resp.status_code == 200
    assert resp.json()["status"] == status
