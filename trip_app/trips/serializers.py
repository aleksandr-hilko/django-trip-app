from core.utils import str_to_geopoint
from django.utils import timezone
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from .models import Trip


class GeoField(serializers.CharField):
    """
    Geo objects to string and vice versa
    """

    def to_representation(self, value):
        """ Convert Point object to string. E.g. Point(23.4, 23.5) -> '[23.4 23.5]' """
        return value.coords

    def to_internal_value(self, data):
        """ Convert string coordinates in Point object. E.g. '23.4 23.5'-> Point(23.4, 23.5) """
        return str_to_geopoint(data)


class TripSerializer(ModelSerializer):
    dest_point = GeoField(required=True, max_length=100)
    start_point = GeoField(required=True, max_length=100)
    driver = serializers.StringRelatedField(read_only=True)
    dist1 = serializers.CharField(required=False, read_only=True)
    dist2 = serializers.CharField(required=False, read_only=True)

    class Meta:
        model = Trip
        fields = [
            "id",
            "driver",
            "passengers",
            "dep_time",
            "start_point",
            "dest_point",
            "price",
            "num_seats",
            "man_approve",
            "description",
            "is_active",
            'dist1',
            'dist2',
        ]
        extra_kwargs = {
            'passengers': {'read_only': True},
            'man_approve': {'write_only': True},
            'is_active': {'write_only': True},
        }

    def validate_dep_time(self, value):
        """
        Check that the departure time is in the future
        """
        if value < timezone.now():
            raise serializers.ValidationError("Departure time has expired. Please correct the time")
        return value
