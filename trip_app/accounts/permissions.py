from rest_framework import permissions


class IsAuthOwnerOrAdminOnly(permissions.IsAuthenticated):
    """ Permissions to allow only owners and admins to get/edit/delete a user.
    """

    def has_object_permission(self, request, view, obj):
        return obj == request.user or request.user.is_superuser
