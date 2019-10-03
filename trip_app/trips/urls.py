from django.urls import path

from .views import TripListCreateApiView

app_name = 'trips'

urlpatterns = [
    path("", TripListCreateApiView.as_view(), name="list_create"),
]
