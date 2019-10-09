from rest_framework.permissions import IsAuthenticated


class IsTripDriverOrAdmin(IsAuthenticated):
    """
    Permissions to allow only driver of a trip or admin to edit/delete a trip
    """

    def has_object_permission(self, request, view, obj):
        return obj.driver == request.user or request.user.is_staff
