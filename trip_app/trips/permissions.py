from rest_framework import permissions


class IsTripDriverOrAdmin(permissions.IsAdminUser):
    """
    Object-level permission to only allow owners of an object to edit it.
    """

    def has_object_permission(self, request, view, obj):
        is_admin = super().has_permission(request, view)
        return obj.driver == request.user or is_admin
