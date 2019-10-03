from django.contrib.gis.geos import fromstr
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from .models import Trip


class GeoField(serializers.CharField):
    """
    Geo objects to string repr and vice versa
    """

    def to_representation(self, value):
        return value.coords

    def to_internal_value(self, data):
        """ Convert string coordinates in Point object. E.g. '23.4 23.5'-> Point(23.4, 23.5) """
        lon, lat = data.split()
        print(data, lon, lat)
        return fromstr(f'POINT({lon} {lat})', srid=4326)


class TripSerializer(ModelSerializer):
    dest_point = GeoField(required=True, max_length=100)
    start_point = GeoField(required=True, max_length=100)
    driver = serializers.StringRelatedField()

    class Meta:
        model = Trip
        fields = ["id", "driver", "passengers", "dep_time", "start_point", "dest_point", "price", "num_seats",
                  "man_approve",
                  "description", "is_active"]
        extra_kwargs = {
            'driver': {'read_only': True},
            'passengers': {'read_only': True},
            'man_approve': {'write_only': True},
            'is_active': {'write_only': True},
        }
