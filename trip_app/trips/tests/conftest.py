from datetime import timedelta

import pytest
from django.utils import timezone

from .trip_factory import TripFactory, faker


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
    data = {
        "dep_time": (timezone.now() + timedelta(days=1)),
        "start_point": f"{faker.latitude()} {float(faker.longitude())}",
        "dest_point": f"{faker.latitude()} {float(faker.longitude())}",
        "price": faker.random_number(),
        "num_seats": faker.random_digit_not_null(),
        "description": "test description",
    }
    return data
