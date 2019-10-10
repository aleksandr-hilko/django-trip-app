import factory
from faker import Factory as FakerFactory
from django.contrib.auth import get_user_model

User = get_user_model()
faker = FakerFactory.create()


class UserFactory(factory.django.DjangoModelFactory):
    """User factory."""
    username = factory.Sequence(lambda n: 'user%d' % n)
    first_name = factory.LazyAttribute(lambda _: faker.first_name())
    last_name = factory.LazyAttribute(lambda _: faker.last_name())
    email = factory.LazyAttribute(lambda _: faker.email())
    is_staff = factory.LazyAttribute(lambda _: False)
    is_active = factory.LazyAttribute(lambda _: False)
    password = factory.LazyAttribute(lambda _: faker.password())

    class Meta:
        model = User
