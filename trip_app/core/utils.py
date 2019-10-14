import re

from django.conf import settings
from django.contrib.gis.geos import Point
from django.contrib.gis.geos import fromstr
from geopy import Nominatim
from rest_framework.exceptions import ValidationError

geolocator = Nominatim(user_agent=settings.OPEN_STREET_MAP_KEY)


def raise_for_status(resp):
    """ Raises an exception if it occurs given response object """

    http_error_msg = ""

    if 400 <= resp.status_code < 500:
        http_error_msg = f"Client Error: {resp.status_code} {resp.json()} for url: {resp.url} "

    elif 500 <= resp.status_code < 600:
        http_error_msg = f"Server Error: {resp.status_code} {resp.json()} for url: {resp.url} "

    if http_error_msg:
        raise Exception(http_error_msg)


def str_to_geopoint(data):
    """ Convert string coordinates into a  Point object.
        Regex is used to handle different incoming formats.
        E.g. '23.4 23.5', '[23.4 23.5]', '(23.4 23.5)' would be converted into
        the same object Point(23.4, 23.5) """
    lon, lat = re.findall(r"[-+]?\d*\.?\d+|\d+", data)
    if not -90 <= float(lon) <= 90:
        raise ValidationError(
            " Longitude coordinates should be in range -90...90 "
        )
    if not -180 <= float(lat) <= 180:
        raise ValidationError(
            " Latitude coordinates should be in range -180...180 "
        )
    return fromstr(f"POINT({lon} {lat})", srid=4326)


def geocode_or_raise_validation_error(address):
    geo_location = geolocator.geocode(f"{address}")
    if not geo_location:
        raise ValidationError(
            "Please correct the address or provide geo coordinates. "
            f"We can't geocode address: {address}"
        )
    return Point(geo_location.latitude, geo_location.longitude, srid=4326)
