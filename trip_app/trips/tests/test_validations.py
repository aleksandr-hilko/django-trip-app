import pytest
from django.contrib.gis.geos import Point
from django.urls import reverse

from .trip_factory import TripFactory
from ..serializers import TripSerializer

MAX_LONGITUDE = 90.0
MAX_LATITUDE = 180.0
MIN_LONGITUDE = -90.0
MIN_LATITUDE = -180.0
CORRECT_LATITUDE = 10
CORRECT_LONGITUDE = 10


@pytest.mark.django_db
@pytest.mark.parametrize('incorrect_coords',
                         [
                             (MIN_LATITUDE - 0.1, CORRECT_LONGITUDE),
                             (CORRECT_LATITUDE, MIN_LONGITUDE - 0.1),
                             (MAX_LATITUDE + 0.1, CORRECT_LONGITUDE),
                             (CORRECT_LATITUDE, MAX_LONGITUDE + 0.1),
                         ]
                         )
def test_unable_to_create_trip_with_incorrect_coords(admin_client, incorrect_coords):
    """  Verify coordinate validations """

    latitude, longitude = incorrect_coords
    start_point = Point(longitude, latitude, srid=4326)
    url = reverse("trips:list_create")
    trip = TripFactory.build(start_point=start_point)
    serializer = TripSerializer(trip)
    resp = admin_client.post(url, json=serializer.data)
    assert resp.status_code == 400
