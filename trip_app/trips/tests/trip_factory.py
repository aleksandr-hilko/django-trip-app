from datetime import timedelta

import factory
from django.contrib.gis.geos import Point
from django.utils import timezone
from faker import Factory as FakerFactory

from accounts.tests.user_factory import UserFactory
from trips.models import Trip

faker = FakerFactory.create()


class TripFactory(factory.django.DjangoModelFactory):
    """Trip factory."""

    driver = factory.SubFactory(UserFactory)
    dep_time = timezone.now() + timedelta(days=1)
    start_point = Point(
        float(faker.latitude()), float(faker.longitude()), srid=4326
    )
    dest_point = Point(
        float(faker.latitude()), float(faker.longitude()), srid=4326
    )
    price = faker.random_number()
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
