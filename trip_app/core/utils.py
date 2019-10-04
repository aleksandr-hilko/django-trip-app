import re

from django.contrib.gis.geos import fromstr


def raise_for_status(resp):
    """ Raises an exception if it occurs given response object """

    http_error_msg = ''

    if 400 <= resp.status_code < 500:
        http_error_msg = f"Client Error: {resp.status_code} {resp.json()} for url: {resp.url} "

    elif 500 <= resp.status_code < 600:
        http_error_msg = f"Server Error: {resp.status_code} {resp.json()} for url: {resp.url} "

    if http_error_msg:
        raise Exception(http_error_msg)


def str_to_geopoint(data):
    """ Convert string coordinates in Point object. E.g. '23.4 23.5'-> Point(23.4, 23.5) """
    lon, lat = re.findall("(\d+(?:\.\d+)?)", data)
    print(data, lon, lat)
    return fromstr(f'POINT({lon} {lat})', srid=4326)
