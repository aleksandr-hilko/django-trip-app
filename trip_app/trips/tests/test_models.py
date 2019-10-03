import pytest
from accounts.tests.user_factory import UserFactory

from .trip_factory import TripFactory
from ..models import Trip


@pytest.fixture(
    params=[0, 1, 10]
)
def passengers(request):
    """ Create multiple users depending on params and return quantity"""
    qty = request.param
    return UserFactory.create_batch(size=qty, is_staff=False)


@pytest.mark.django_db(transaction=True)
class TestTrips:
    def test_create_trip(self):
        """ Verify that Trip model can be created with all expected attributes """
        exp_trip = TripFactory()
        assert Trip.objects.count() == 1
        act_trip = Trip.objects.first()
        assert act_trip.driver == exp_trip.driver
        assert act_trip.dep_time == exp_trip.dep_time
        assert act_trip.start_point == exp_trip.start_point
        assert act_trip.dest_point == exp_trip.dest_point
        assert act_trip.price == exp_trip.price
        assert act_trip.num_seats == exp_trip.num_seats
        assert act_trip.man_approve is exp_trip.man_approve
        assert act_trip.description == exp_trip.description
        assert act_trip.created == exp_trip.created

    def test_create_trip_with_passengers(self, passengers):
        """ Verify that trip can be created with multiple passengers """
        TripFactory.create(passengers=passengers)
        passengers_count = len(passengers)
        assert Trip.objects.count() == 1
        act_trip = Trip.objects.first()
        assert act_trip.passengers.count() == passengers_count
        new_user = UserFactory()
        act_trip.passengers.add(new_user)
        assert act_trip.passengers.count() == passengers_count + 1

    def test_add_passenger_to_trip(self):
        """ Verify that passenger can be added to the trip """
        trip = TripFactory.create()
        assert Trip.objects.count() == 1
        act_trip = Trip.objects.first()
        assert trip.id == trip.id
        assert act_trip.passengers.count() == 0
        new_user = UserFactory()
        act_trip.passengers.add(new_user)
        assert act_trip.passengers.count() == 1
