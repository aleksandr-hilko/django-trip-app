import pytest

from trips.models import TripRequest


@pytest.mark.django_db
class TestTripModel:
    def test_approve(self, trip_request):
        """ Verify TripRequest model 'approve' method. """
        trip_request.approve()
        trip_request = TripRequest.objects.get(id=trip_request.id)
        assert trip_request.status == TripRequest.APPROVED
        assert trip_request.user in trip_request.trip.passengers.all()

    def test_decline(self, trip_request):
        """ Verify TripRequest model 'decline' method. """
        trip_request.decline()
        trip_request = TripRequest.objects.get(id=trip_request.id)
        assert trip_request.status == TripRequest.DECLINED

    def test_cancel_active(self, trip_request):
        """ Verify TripRequest model 'cancel' method for 'Active' status. """
        trip_request.cancel()
        trip_request = TripRequest.objects.get(id=trip_request.id)
        assert trip_request.status == TripRequest.INACTIVE

    def test_cancel_approved(self, trip_request):
        """ Verify TripRequest model 'cancel' method for 'Approved' status. """
        trip_request.approve()
        trip_request.cancel()
        trip_request = TripRequest.objects.get(id=trip_request.id)
        assert trip_request.status == TripRequest.INACTIVE
        assert trip_request.user not in trip_request.trip.passengers.all()
