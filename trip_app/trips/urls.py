from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register("trips", views.TripViewSet, base_name="trips")
router.register(
    "trip-requests", views.TripRequestViewSet, base_name="trip-requests"
)

urlpatterns = [path("", include(router.urls))]
