from rest_framework import permissions


class IsAuthOwnerOrAdminOnly(permissions.IsAuthenticated):
    """
    Custom permission to only allow owners and admins to get/edit it.
    """

    def has_object_permission(self, request, view, obj):
        # Write permissions are only allowed to the owner or admin
        is_auth = super().has_object_permission(request, view, obj)
        return (is_auth and obj == request.user) or (is_auth and request.user.is_superuser)
