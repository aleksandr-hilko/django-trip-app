from django.contrib import admin
from django.contrib.gis.admin import OSMGeoAdmin

from trips.models import Trip


@admin.register(Trip)
class TripAdmin(OSMGeoAdmin):
    list_display = (
        "id",
        "driver",
        "get_passengers",
        "dep_time",
        "start_point",
        "dest_point",
        "price",
        "num_seats",
        "man_approve",
        "description",
    )
