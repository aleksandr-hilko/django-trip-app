import pytest
from django.contrib.auth import get_user_model
from django.db import IntegrityError

from . import user_factory

User = get_user_model()


@pytest.mark.django_db(transaction=True)
class TestUsers:
    @pytest.mark.parametrize('user__is_staff', [True, False])
    def test_create_user_staff(self, user__is_staff):
        """ Verify the ability to create a staff/non staff user """
        user_factory.UserFactory(is_staff=user__is_staff)
        assert User.objects.count() == 1
        user = User.objects.first()
        assert user.is_staff is user__is_staff

    @pytest.mark.parametrize('is_active', [True, False])
    def test_create_user_active_create(self, is_active):
        """ Verify the ability to create a active/inactive user"""
        user_factory.UserFactory(is_active=is_active)
        assert User.objects.count() == 1
        user = User.objects.first()
        assert user.is_active is is_active

    def test_unable_to_create_user_with_existing_name(self):
        """ Verify that exception will be raised when the user with the existing user name is created """
        name = "test_name"
        user_factory.UserFactory(username=name)
        with pytest.raises(IntegrityError) as exc:
            user_factory.UserFactory(username=name, is_staff=False)
            assert 'UNIQUE constraint failed:' in exc

    def test_create_user_with_blank_fields(self):
        """ Verify the ability to create a user with blank first name, last name and email """
        user_factory.UserFactory(first_name="", last_name="", email="")
        assert User.objects.count() == 1
        user = User.objects.first()
        assert user.first_name == ""
        assert user.last_name == ""
        assert user.email == ""
