from django.urls import path
from .views import ListCreateTrip

app_name = 'trips'

urlpatterns = [
    path("", ListCreateTrip.as_view(), name="list_create"),
]
