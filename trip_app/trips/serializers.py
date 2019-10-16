from django.utils import timezone
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.serializers import ModelSerializer
from rest_framework_gis import fields as geofields
from rest_framework_gis.serializers import GeoFeatureModelSerializer

from core.utils import geocode_or_validation_error, validate_geo_point
from trips.models import Trip, TripRequest, Location


class LocationSerializer(GeoFeatureModelSerializer):
    """ A class to serialize locations as GeoJSON compatible data """

    point = geofields.GeometryField(required=False)

    def validate_point(self, value):
        """ Point field validation. """
        validate_geo_point(value.x, value.y)
        return value

    def validate(self, attrs):
        """ Object level validation.

            First verify that at least one location attribute is provided,
            if no geo coordinate is provided, verify that address can be
            geocoded.
            """
        if not any(value for value in attrs.values()):
            raise ValidationError("Specify either address or geo coords")
        if not attrs.get("point"):
            address = attrs["address"]
            geocode_or_validation_error(address)
        return attrs

    def create(self, validated_data):
        """ Override of the base create method.

            If no geo coordinate is provided, geocode the address and save
            the model, otherwise just call base create() to save the model.
            """
        if not validated_data.get("point"):
            address = validated_data["address"]
            validated_data["point"] = geocode_or_validation_error(address)
        return super().create(validated_data)

    def update(self, instance, validated_data):
        """ Override of the base update method.

            If no geo coordinate is provided, geocode the address and save
            the model, otherwise just call base update() to update the model.
            """
        if not validated_data.get("point"):
            address = validated_data["address"]
            validated_data["point"] = geocode_or_validation_error(address)
        return super().update(instance, validated_data)

    class Meta:
        model = Location
        geo_field = "point"
        fields = ("id", "address", "point")


class TripSerializer(ModelSerializer):
    dest_point = LocationSerializer()
    start_point = LocationSerializer()
    driver = serializers.StringRelatedField(read_only=True)
    passengers = serializers.StringRelatedField(read_only=True, many=True)
    dist1 = serializers.CharField(required=False, read_only=True)
    dist2 = serializers.CharField(required=False, read_only=True)
    free_seats = serializers.SerializerMethodField(read_only=True)

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
            "free_seats",
            "man_approve",
            "description",
            "is_active",
            "dist1",
            "dist2",
        ]
        extra_kwargs = {"num_seats": {"write_only": True}}

    def create(self, validated_data):
        """ Overwrite the base create method in order to explicitly
            handle nested serializers relationships.
            """
        start_point_data, dest_point_data = (
            validated_data.get("start_point"),
            validated_data.get("dest_point"),
        )

        validated_data["start_point"] = LocationSerializer().create(
            validated_data=start_point_data
        )
        validated_data["dest_point"] = LocationSerializer().create(
            validated_data=dest_point_data
        )

        return super().create(validated_data)

    def update(self, instance, validated_data):
        """ Overwrite the base update method in order to explicitly
            handle nested serializers relationships.
            """
        start_point_data, dest_point_data = (
            validated_data.get("start_point"),
            validated_data.get("dest_point"),
        )

        if start_point_data:
            validated_data["start_point"] = LocationSerializer().update(
                instance=instance.start_point, validated_data=start_point_data
            )

        if dest_point_data:
            validated_data["dest_point"] = LocationSerializer().update(
                instance=instance.dest_point, validated_data=dest_point_data
            )

        return super().update(instance=instance, validated_data=validated_data)

    def get_free_seats(self, obj):
        return obj.free_seats

    def validate_dep_time(self, value):
        """
        Check that the departure time is in the future.
        """
        if value < timezone.now():
            raise serializers.ValidationError(
                "Departure time has expired. Please correct the time."
            )
        return value


class TripRequestSerializer(ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = TripRequest
        fields = ["id", "trip", "user"]
