import pytest
from django.urls import reverse


@pytest.mark.django_db
class TestTripPermissions:
    def test_unable_update(self, client_user, trip):
        """ Verify that authenticated non driver, non admin can't update
            trip with PATCH api/trips/<trip_id>/. """
        client, _ = client_user
        url = reverse("trips-detail", args=[trip.id])
        resp = client.patch(
            url, {"price": 20}, content_type="application/json"
        )
        assert resp.status_code == 403

    def test_unable_delete(self, client_user, trip):
        """ Verify that authenticated non driver, non admin can't delete
            trip with DELETE api/trips/<trip_id>/.  """
        client, _ = client_user
        url = reverse("trips-detail", args=[trip.id])
        resp = client.delete(url)
        assert resp.status_code == 403

    def test_driver_delete(self, client_trip):
        """ Verify that driver can delete it's own trip with
            DELETE api/trips/<trip_id>/. """
        client, trip = client_trip
        url = reverse("trips-detail", args=[trip.id])
        resp = client.delete(url)
        assert resp.status_code == 204

    def test_driver_update(self, client_trip):
        """ Verify that driver can delete it's own trip
            with PATCH api/trips/<trip_id>/. """
        client, trip = client_trip
        url = reverse("trips-detail", args=[trip.id])
        resp = client.patch(
            url, {"price": 20.00}, content_type="application/json"
        )
        assert resp.status_code == 200
        assert float(resp.json()["price"]) == 20.00

    def test_admin_delete(self, admin_client, trip):
        """ Verify that admin can delete trip with
            DELETE api/trips/<trip_id>/. """
        url = reverse("trips-detail", args=[trip.id])
        resp = admin_client.delete(url)
        assert resp.status_code == 204

    @pytest.mark.parametrize(
        "url", ["trip-requests-approve", "trip-requests-decline"]
    )
    def test_user_unable_approve_decline(self, client_user, url, trip_request):
        """ Verify that authenticated non driver, non admin can't approve(decline)
            trip request with POST api/trip-requests/<id>/approve(decline). """
        client, _ = client_user
        request_url = reverse(url, args=[trip_request.id])
        resp = client.post(request_url)
        assert resp.status_code == 403

    @pytest.mark.parametrize(
        "url, status",
        [
            ("trip-requests-approve", "Approved"),
            ("trip-requests-decline", "Declined"),
        ],
    )
    def test_owner_approve_decline(self, client_request_driver, url, status):
        """ Verify that driver can approve(decline) trip request with
            POST api/trip-requests/<id>/approve(decline). """
        client, trip_request = client_request_driver
        request_url = reverse(url, args=[trip_request.id])
        resp = client.post(request_url)
        assert resp.status_code == 200
        assert resp.json()["status"] == status

    def test_reserve_multiple(self, client_request_user):
        """ Verify that user is forbidden to reserve a trip for which
            user request already exists. """
        client, trip_request = client_request_user
        reserve_trip_url = reverse(
            "trips-reserve", args=[trip_request.trip.id]
        )
        resp = client.post(reserve_trip_url)
        assert resp.status_code == 403

    def test_driver_reserve(self, client_trip):
        """ Verify that driver is forbidden to reserve a trip to
            POST /api/trips/<trip_id>/reserve/. """
        client, trip = client_trip
        url = reverse("trips-reserve", args=[trip.id])
        resp = client.post(url)
        assert resp.status_code == 403
