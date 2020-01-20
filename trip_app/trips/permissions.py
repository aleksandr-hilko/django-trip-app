from rest_framework.permissions import IsAuthenticated
from trips.models import TripRequest


class IsTripDriverOrAdmin(IsAuthenticated):
    """ Permissions to allow only driver of a trip or admin to edit a trip. """

    def has_object_permission(self, request, view, obj):
        return obj.driver == request.user or request.user.is_staff


class IsRequestDriverOrAdmin(IsAuthenticated):
    """ Permissions to allow only driver or admin
       to edit a trip request. """

    def has_object_permission(self, request, view, obj):
        return obj.trip.driver == request.user or request.user.is_staff


class IsRequestUserOrAdmin(IsAuthenticated):
    """ Permissions to allow only a user who requested a trip or admin
        to edit a trip request. """

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user or request.user.is_staff


class NewPassengerNotDriver(IsAuthenticated):
    """ Permissions to allow only a new passenger and not a driver to
        request a trip. """

    def has_object_permission(self, request, view, obj):
        already_requested = (
            request.user.requests.filter(trip_id=obj.id)
            .exclude(status__in=[TripRequest.INACTIVE, TripRequest.DECLINED])
            .exists()
        )
        return not already_requested and not request.user == obj.driver
