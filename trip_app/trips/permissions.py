from rest_framework.permissions import IsAuthenticated


class IsTripDriverOrAdmin(IsAuthenticated):
    """
    Object-level permission to only allow owners of an object to edit it.
    """

    def has_object_permission(self, request, view, obj):
        return obj.driver == request.user or request.user.is_staff
