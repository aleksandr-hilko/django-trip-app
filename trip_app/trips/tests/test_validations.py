import datetime

import pytest
from django.contrib.gis.geos import Point
from django.urls import reverse
from django.utils import timezone

from core.utils import str_to_geopoint

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
    start_point = f"{longitude}, {latitude}"
    trip_data["start_point"] = start_point
    resp = admin_client.post(list_create_trips_url, trip_data)
    assert resp.status_code == 400
    assert (
        f"{incorrect_arg} coordinates should be in range "
        in resp.json()["start_point"][0]
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
    """ Verify 'str_to_geopoint' function that is responsible for serializing incoming
        string coordinates to django.contrib.gis.geos.Point objects"""
    point = str_to_geopoint(str_coord)
    assert point == Point(23.5, 23.5, srid=4326)
    assert point.x == 23.5
    assert point.y == 23.5
