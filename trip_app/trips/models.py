from django.conf import settings
from django.contrib.gis.db import models as geo_models
from django.db import models


class Location(models.Model):
    address = models.CharField(max_length=150, blank=True)
    point = geo_models.PointField()


class Trip(models.Model):
    driver = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="suggested_trips",
        on_delete=models.CASCADE,
    )
    passengers = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name="booked_trips"
    )
    dep_time = models.DateTimeField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    start_point = models.ForeignKey(
        Location,
        related_name="start_point_of",
        on_delete=models.SET_NULL,
        null=True,
    )
    dest_point = models.ForeignKey(
        Location,
        related_name="dest_point_of",
        on_delete=models.SET_NULL,
        null=True,
    )
    num_seats = models.PositiveIntegerField()
    man_approve = models.BooleanField(default=True)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)

    @property
    def free_seats(self):
        """ Number of free seats that remained for the trip. """
        return self.num_seats - self.passengers.count()

    def get_passengers(self):
        return ",".join([str(p) for p in self.passengers.all()])


class TripRequest(models.Model):
    ACTIVE = 1
    APPROVED = 2
    DECLINED = 3
    STATUS_CHOICES = [
        (ACTIVE, 'Active'),
        (APPROVED, 'Approved'),
        (DECLINED, 'Declined'),
    ]
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE, related_name="requests")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="requests")
    status = models.IntegerField(choices=STATUS_CHOICES, default=ACTIVE)
    created = models.DateTimeField(auto_now_add=True)
