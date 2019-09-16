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

class IsAdminOrOwner(BasePermission):
    """
    The request is authenticated as a Admin, or Author of the book .
    can only be used  in
    """
    def has_permission(self, request, view):
        """
        Return `True` if permission is granted, `False` otherwise.
        """
        return True

    def has_object_permission(self, request, view, obj):
        return bool(
            request.method in SAFE_METHODS or
            request.user.is_superuser or
            request.user.id == obj.created_by.id
        )