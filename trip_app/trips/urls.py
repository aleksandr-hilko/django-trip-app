from django.urls import path
from .views import CreateTripView, ListTripView

app_name = 'trips'

urlpatterns = [
    path("", CreateTripView.as_view(), name="create"),
    path("", ListTripView.as_view(), name="create"),
]
