import pytest

from trips.models import TripRequest
from trips.tests.trip_factory import TripRequestFactory


@pytest.mark.django_db
def test_approve():
    """ Verify TripRequest model 'approve' method. """
    trip_request = TripRequestFactory(status=TripRequest.ACTIVE)
    trip_request.approve()
    trip_request = TripRequest.objects.get(id=trip_request.id)
    assert trip_request.status == TripRequest.APPROVED
    assert trip_request.user in trip_request.trip.passengers.all()


@pytest.mark.django_db
def test_decline():
    """ Verify TripRequest model 'decline' method. """
    trip_request = TripRequestFactory(status=TripRequest.ACTIVE)
    trip_request.decline()
    trip_request = TripRequest.objects.get(id=trip_request.id)
    assert trip_request.status == TripRequest.DECLINED


@pytest.mark.django_db
def test_cancel_active():
    """ Verify TripRequest model 'cancel' method for 'Active' status. """
    trip_request = TripRequestFactory(status=TripRequest.ACTIVE)
    trip_request.cancel()
    trip_request = TripRequest.objects.get(id=trip_request.id)
    assert trip_request.status == TripRequest.INACTIVE


@pytest.mark.django_db
def test_cancel_approved():
    """ Verify TripRequest model 'cancel' method for 'Approved' status. """
    trip_request = TripRequestFactory(status=TripRequest.ACTIVE)
    trip_request.approve()
    trip_request.cancel()
    trip_request = TripRequest.objects.get(id=trip_request.id)
    assert trip_request.status == TripRequest.INACTIVE
    assert trip_request.user not in trip_request.trip.passengers.all()
