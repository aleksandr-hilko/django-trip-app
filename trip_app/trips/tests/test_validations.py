import datetime

import pytest
from django.contrib.gis.geos import Point
from django.urls import reverse
from django.utils import timezone
from rest_framework.exceptions import ValidationError

from core.utils import str_to_geopoint, geocode_or_raise_validation_error
from trips.serializers import LocationSerializer

MAX_LONGITUDE = 90.0
MAX_LATITUDE = 180.0
MIN_LONGITUDE = -90.0
MIN_LATITUDE = -180.0
CORRECT_LATITUDE = 10
CORRECT_LONGITUDE = 10

list_create_trips_url = reverse("trips-list")


@pytest.mark.django_db
@pytest.mark.parametrize(
    "incorrect_coords",
    [
        [CORRECT_LONGITUDE, MIN_LATITUDE - 0.1, "Latitude"],
        [MIN_LONGITUDE - 0.1, CORRECT_LATITUDE, "Longitude"],
        [CORRECT_LONGITUDE, MAX_LATITUDE + 0.1, "Latitude"],
        [MAX_LONGITUDE + 0.1, CORRECT_LATITUDE, "Longitude"],
    ],
)
def test_incorrect_coords(admin_client, incorrect_coords, trip_data):
    """ Verify that Trip can't be created having incorrect coordinate """
    longitude, latitude, incorrect_arg = incorrect_coords
    start_point = f"POINT({latitude} {longitude})"
    trip_data["start_point"]["point"] = start_point
    resp = admin_client.post(
        list_create_trips_url, trip_data, content_type="application/json"
    )
    assert resp.status_code == 400
    assert (
        f"{incorrect_arg} coordinates should be in range "
        in resp.json()["start_point"]["point"][0]
    )


def test_invalid_dep_time(admin_client, trip_data):
    """ Verify that Trip can't be created with expired departure time"""
    time_in_the_past = timezone.now() - datetime.timedelta(minutes=30)
    trip_data["dep_time"] = time_in_the_past.strftime("%Y-%m-%dT%H:%M:%S")
    resp = admin_client.post(list_create_trips_url, trip_data)
    assert resp.status_code == 400
    assert "Departure time has expired" in resp.json()["dep_time"][0]


@pytest.mark.parametrize(
    "str_coord",
    ["23.5 23.5", "[23.5 23.5]", "[23.5, 23.5]", "(23.5, 23.5)", "23.5, 23.5"],
)
def test_convert_to_geopoint(str_coord):
    """ Verify 'str_to_geopoint' function that is responsible for serializing
    incoming string coordinates to django.contrib.gis.geos.Point objects. """
    point = str_to_geopoint(str_coord)
    assert point == Point(23.5, 23.5, srid=4326)
    assert point.x == 23.5
    assert point.y == 23.5


@pytest.mark.parametrize(
    "address",
    [
        "Минск Советская",
        "Гродно Советская",
        "Могилёв Советская",
        "Витебск Советская",
        "Гомель Советская",
        "Брест Советская",
    ],
)
def test_geocode(address):
    """ Verify 'geocode_or_raise_validation_error' can geocode address. """
    point = geocode_or_raise_validation_error(address)
    assert point


@pytest.mark.parametrize(
    "invalid_address", ["absolute_fake", "asd12fe34", "123123123123123324"]
)
def test_invalid_geocode(invalid_address):
    """ Verify that 'geocode_or_raise_validation_error' function
        raises Validation error for invalid address. """
    with pytest.raises(ValidationError) as exc:
        geocode_or_raise_validation_error(invalid_address)
    assert f"We can't geocode address: {invalid_address}" in str(exc.value)


def test_empty_location():
    """ Verify that error is raised when
        nor address or geo coords are provided. """
    data = {}
    serializer = LocationSerializer(data=data)
    with pytest.raises(ValidationError) as exc:
        serializer.is_valid(raise_exception=True)
    assert "Specify either address or geo coords" in str(exc.value)
