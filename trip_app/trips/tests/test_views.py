from datetime import timedelta

import pytest
from django.contrib.gis.geos import Point
from django.urls import reverse
from django.utils import timezone

from .trip_factory import TripFactory
from ..views import TripViewSet

list_create_trips_url = reverse("trips-list")


@pytest.fixture
def trips_with_different_dep_times():
    """ Create 2 trips with different dep time to test against them """
    dep_time_1 = timezone.now() + timedelta(minutes=30)
    dep_time_2 = timezone.now() + timedelta(minutes=10)
    trip_1 = TripFactory(dep_time=dep_time_1)
    trip_2 = TripFactory(dep_time=dep_time_2)
    return trip_1, trip_2


@pytest.fixture
def trips_with_different_coordinates():
    """ Create 5 trips with different start and dest points.
        For all of them start point is the same in minsk, and  dest points are different.
        Return created trips in order of increasing distance between start and destination points.
        (E.g. Minsk - Grodno is the minimum distance, whereas Minsk - Magadan is the maximum) """
    minsk_point = Point(53.910206, 27.566264, srid=4326)
    grodno_point = Point(53.669742, 23.822384, srid=4326)
    warsaw_point = Point(52.219361, 21.013097, srid=4326)
    berlin_point = Point(52.514257, 13.403819, srid=4326)
    london_point = Point(51.510363, -0.124398, srid=4326)
    lissabon_point = Point(38.719013, -9.224802, srid=4326)
    minsk_grodno = TripFactory(start_point=minsk_point, dest_point=grodno_point)
    minsk_warsaw = TripFactory(start_point=minsk_point, dest_point=warsaw_point)
    minsk_berlin = TripFactory(start_point=minsk_point, dest_point=berlin_point)
    minsk_london = TripFactory(start_point=minsk_point, dest_point=london_point)
    minsk_lissabon = TripFactory(start_point=minsk_point, dest_point=lissabon_point)
    return minsk_grodno, minsk_warsaw, minsk_berlin, minsk_london, minsk_lissabon


@pytest.mark.django_db
def test_create_trip(admin_client, trip_data):
    resp = admin_client.post(list_create_trips_url, trip_data)
    assert resp.status_code == 201
    trip_dict = resp.json()
    assert trip_dict["driver"] == "admin"
    assert trip_dict["dep_time"] == trip_data["dep_time"]
    assert trip_dict["start_point"] == trip_data["start_point"]
    assert trip_dict["dest_point"] == trip_data["dest_point"]
    assert trip_dict["price"] == trip_data["price"]
    assert trip_dict["num_seats"] == trip_data["num_seats"]
    assert trip_dict["description"] == trip_data["description"]


@pytest.mark.django_db
def test_get_trips_filtering_time(admin_client, trips):
    """ Verify that correct number of trips is created and returned queryset
        is limited to the page_size parameter or TripListCreateApiView """
    trips_count = len(trips)
    resp = admin_client.get(list_create_trips_url)
    assert resp.status_code == 200
    trip_dict = resp.json()
    assert trip_dict["count"] == trips_count
    max_page_size = TripViewSet.pagination_class.page_size

    if trips_count > max_page_size:
        assert len(trip_dict["results"]) == max_page_size
    else:
        assert len(trip_dict["results"]) == trips_count


@pytest.mark.django_db
def test_filter_trips_by_distance(admin_client, trips_with_different_coordinates):
    """ Verify that trips are filtered correctly by minimum distance between user coordinates and trips coordinates """
    exp_trip_order = [trip.id for trip in trips_with_different_coordinates]
    user_sp, user_dp = trips_with_different_coordinates[0].start_point, trips_with_different_coordinates[0].dest_point
    resp = admin_client.get(f"{list_create_trips_url}?sp={user_sp.x},{user_sp.y}&dp={user_dp.x},{user_dp.y}")
    assert resp.status_code == 200
    resp_dict = resp.json()
    assert resp_dict['count'] == 5
    results_dict = resp_dict['results']
    act_trip_order = [trip["id"] for trip in results_dict]
    assert act_trip_order == exp_trip_order
    # As user start and destination points are the same as for trip 1
    # the dist1 and dist2 parameters should be 0
    assert results_dict[0]["dist1"] == '0.0 m'
    assert results_dict[0]["dist2"] == '0.0 m'


@pytest.mark.django_db
def test_filter_trips_by_time(admin_client, trips_with_different_dep_times):
    """ Verify that trips are filtered correctly by time and
        trips that are between time1 and time2 interval are returned """
    too_late_trip, in_time_trip = trips_with_different_dep_times
    now = timezone.now()
    # Time points between which we are looking for a trips
    time_1_str = now.strftime("%Y-%m-%dT%H:%M:%S")
    time_2_str = (now + timedelta(minutes=20)).strftime("%Y-%m-%dT%H:%M:%S")
    resp = admin_client.get(f"{list_create_trips_url}?time1={time_1_str}&time2={time_2_str}")
    assert resp.status_code == 200
    resp_dict = resp.json()
    assert resp_dict["count"] == 1
    assert resp_dict["results"][0]["id"] == in_time_trip.id


@pytest.mark.django_db
def test_get_trip(admin_client):
    """ Verify that correct trip data can be accessed via GET /api/trips/<trip_id>/ """
    trip = TripFactory()
    url = reverse("trips-detail", args=[trip.id])
    resp = admin_client.get(url)
    assert resp.status_code == 200
    resp_dict = resp.json()
    assert resp_dict["driver"] == trip.driver.username
    assert resp_dict["start_point"] == f"{trip.start_point.x} {trip.start_point.y}"
    assert resp_dict["dest_point"] == f"{trip.dest_point.x} {trip.dest_point.y}"
    assert resp_dict["price"] == trip.price
    assert resp_dict["num_seats"] == trip.num_seats
    assert resp_dict["description"] == trip.description


@pytest.mark.django_db
def test_update_trip(admin_client, trip_data):
    """ Verify that trip can be updated via PUT /api/trips/<trip_id>/ """
    trip = TripFactory()
    url = reverse("trips-detail", args=[trip.id])
    resp = admin_client.put(url, trip_data, content_type='application/json')
    resp_dict = resp.json()
    assert resp.status_code == 200
    assert resp_dict["start_point"] == trip_data["start_point"]
    assert resp_dict["dest_point"] == trip_data["dest_point"]
    assert resp_dict["price"] == trip_data["price"]
    assert resp_dict["num_seats"] == trip_data["num_seats"]
    assert resp_dict["description"] == trip_data["description"]


@pytest.mark.django_db
def test_delete_trip(admin_client):
    """ Verify that trip can be delete via DELETE /api/trips/<trip_id>/ """
    trip = TripFactory()
    url = reverse("trips-detail", args=[trip.id])
    resp = admin_client.delete(url)
    assert resp.status_code == 204
    resp = admin_client.get(url)
    assert resp.status_code == 404

