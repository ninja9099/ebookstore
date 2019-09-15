from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAdminOrIsSelf(BasePermission):
    """
    The request is authenticated as a Admin, or user  is self .
    """
    def has_object_permission(self, request, view, obj):
        return bool(
            request.method in SAFE_METHODS or
            request.user.is_superuser or
            request.user.id == obj.id
        )