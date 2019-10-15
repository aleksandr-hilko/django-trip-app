import pytest

from .user_factory import UserFactory


@pytest.fixture(params=[0, 1, 10, 100])
def user_create_quantity(request):
    """ Create multiple users depending on params and return quantity"""
    qty = request.param
    UserFactory.create_batch(size=qty, is_staff=False)
    return qty
