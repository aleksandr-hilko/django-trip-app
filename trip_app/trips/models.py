from django.conf import settings
from django.contrib.gis.db import models as geo_models
from django.db import models


class Trip(models.Model):
    driver = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="suggested_trips", on_delete=models.CASCADE)
    passengers = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="booked_trips")
    dep_time = models.DateTimeField()
    start_point = geo_models.PointField()
    dest_point = geo_models.PointField()
    price = models.PositiveIntegerField(null=True)
    num_seats = models.PositiveIntegerField()
    man_approve = models.BooleanField(default=True)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)


class TripRequest(models.Model):
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
