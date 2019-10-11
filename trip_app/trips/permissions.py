from rest_framework.permissions import IsAuthenticated


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
