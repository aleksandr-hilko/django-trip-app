import random
from datetime import timedelta

import pytest
from django.utils import timezone

from core.constants import User
from trips.models import TripRequest
from trips.tests.trip_factory import TripFactory, faker, TripRequestFactory


@pytest.fixture(params=[3, 10])
def trips(request):
    """ Create multiple trips depending on params.
       :return: List of created objects. """
    qty = request.param
    return TripFactory.create_batch(size=qty)


@pytest.fixture
def trip_data():
    """ Create a trip model without touching database and return its dict
        repr for using as a request payload. """
    data = {
        "dep_time": (timezone.now() + timedelta(days=1)),
        "start_point": {
            "point": {"type": "Point", "coordinates": [5.000000, 23.000000]}
        },
        "dest_point": {
            "point": {"type": "Point", "coordinates": [10.000000, 23.000000]}
        },
        "price": round(random.uniform(1, 10000), 2),
        "num_seats": faker.random_digit_not_null(),
        "description": "test description",
    }
    return data


@pytest.fixture
def trip():
    """ Create Trip model in DB. """
    return TripFactory()


@pytest.fixture
def trip_auto_appr():
    """ Create Trip model with auto approve in DB. """
    return TripFactory(man_approve=False)


@pytest.fixture
def trip_request():
    """ Create TripRequest model with active status in DB. """
    return TripRequestFactory(status=TripRequest.ACTIVE)


@pytest.fixture
def client_user(client, create_user):
    """ Create a user and authenticate client with user credentials.
        :returns: Auth client with user object he was authenticated under. """
    pk, username, password = create_user
    user = User.objects.get(pk=pk)
    client.login(username=username, password=password)
    return client, user


@pytest.fixture
def client_trip(client_user):
    """ Create a trip which driver is client user.
        :returns: Auth client with created trip. """
    client, user = client_user
    return client, TripFactory(driver=user)


@pytest.fixture
def client_request_driver(client_trip):
    """ Create a trip request with trip whose driver is client user.
        :returns: Auth client with created trip request. """
    client, trip = client_trip
    return client, TripRequestFactory(trip=trip)


@pytest.fixture
def client_request_user(client_user):
    """ Create a trip request whose user is client user.
        :returns: Auth client with created trip request. """
    client, user = client_user
    return client, TripRequestFactory(user=user)
