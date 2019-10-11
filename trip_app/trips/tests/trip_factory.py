import random
from datetime import timedelta

import factory
from django.contrib.gis.geos import Point
from django.utils import timezone
from faker import Factory as FakerFactory

from accounts.tests.user_factory import UserFactory
from trips.models import Trip, Location, TripRequest

faker = FakerFactory.create()


class LocationFactory(factory.django.DjangoModelFactory):
    """ Location factory. """

    address = faker.address()
    point = Point(float(faker.latitude()), float(faker.longitude()), srid=4326)

    class Meta:
        model = Location


class TripFactory(factory.django.DjangoModelFactory):
    """Trip factory."""

    driver = factory.SubFactory(UserFactory)
    dep_time = timezone.now() + timedelta(days=1)
    start_point = factory.SubFactory(LocationFactory)
    dest_point = factory.SubFactory(LocationFactory)
    price = round(random.uniform(1, 10000), 2)
    num_seats = faker.random_digit_not_null()
    description = "test description"

    @factory.post_generation
    def passengers(self, create, extracted, **kwargs):
        """This is to handle many to many relation between Trip and User model"""
        if not create:
            # When calling TripFactory() or TripFactory.build(),
            # no group binding will be created.
            return

        if extracted:
            # But when TripFactory.create(passengers=(passenger) is called then
            # passengers declaration will add passed in passengers list
            for passenger in extracted:
                self.passengers.add(passenger)

    class Meta:
        model = Trip


class TripRequestFactory(factory.django.DjangoModelFactory):
    trip = factory.SubFactory(TripFactory)
    user = factory.SubFactory(UserFactory)

    class Meta:
        model = TripRequest
