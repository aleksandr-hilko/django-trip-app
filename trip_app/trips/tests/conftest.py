import pytest

from ..serializers import TripSerializer
from .trip_factory import TripFactory


@pytest.fixture(
    params=[3, 10]
)
def trips(request):
    """ Create multiple trips depending on params and return created objects """
    qty = request.param
    return TripFactory.create_batch(size=qty)


@pytest.fixture
def trip_data():
    """ Create a trip model without touching database and return its dict
        repr for using as a request payload """
    trip = TripFactory.build()
    serializer = TripSerializer(trip)
    data = serializer.data
    del data["id"]
    del data["driver"]
    del data["passengers"]
    return data
