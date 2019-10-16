import random
from datetime import timedelta

import pytest
from django.utils import timezone

from .trip_factory import TripFactory, faker


@pytest.fixture(params=[3, 10])
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
        "start_point": {
            "point": {"type": "Point", "coordinates": [5.000000, 23.000000]}
        },
        "dest_point": {
            "point": {"type": "Point", "coordinates": [5.000000, 23.000000]}
        },
        "price": round(random.uniform(1, 10000), 2),
        "num_seats": faker.random_digit_not_null(),
        "description": "test description",
    }
    return data
