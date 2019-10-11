from django.conf import settings
from django.contrib.gis.db import models as geo_models
from django.db import models


class Location(models.Model):
    address = models.CharField(max_length=150, blank=True)
    point = geo_models.PointField()


class Trip(models.Model):
    driver = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="trip_offers",
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
    created = models.DateTimeField(auto_now_add=True)

    @property
    def free_seats(self):
        """ Number of free seats that remained for the trip. """
        return self.num_seats - self.passengers.count()

    def get_passengers(self):
        """ String representation of trip passengers. """
        return ",".join([str(p) for p in self.passengers.all()])


class TripRequest(models.Model):
    ACTIVE = 1
    APPROVED = 2
    DECLINED = 3
    INACTIVE = 4
    STATUS_CHOICES = [
        (ACTIVE, "Active"),
        (APPROVED, "Approved"),
        (DECLINED, "Declined"),
        (INACTIVE, "Inactive"),
    ]
    trip = models.ForeignKey(
        Trip, on_delete=models.CASCADE, related_name="requests"
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="requests",
    )
    status = models.IntegerField(choices=STATUS_CHOICES, default=ACTIVE)
    created = models.DateTimeField(auto_now_add=True)

    def approve(self):
        """ Set "Approved" status in DB
            and add user to trip's passenger list. """
        self.status = TripRequest.APPROVED
        self.save()
        self.trip.passengers.add(self.user)
        self.trip.save()

    def decline(self):
        """ Set "Declined" status for a model in DB
            and remove user from a trip's passenger list. """
        self.status = TripRequest.DECLINED
        self.save()
        if self.user in self.trip.passengers.all():
            self.trip.passengers.remove(self.user)
            self.trip.save()

    def cancel(self):
        """ Set "Inactive" status for a model in DB
            and remove user from trip's passenger list. """
        self.status = TripRequest.INACTIVE
        self.save()
        if self.user in self.trip.passengers.all():
            self.trip.passengers.remove(self.user)
            self.trip.save()
