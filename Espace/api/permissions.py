from rest_framework.permissions import (BasePermission, IsAdminUser,
                                        SAFE_METHODS)


class isOwnerOrAdmin(BasePermission):
    """This class creates permissions for delete and update methods"""

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user or request.user.is_staff or obj.id == request.user.id  # noqa


class IsAdminUserOrReadOnly(IsAdminUser):
    def has_permission(self, request, view):
        is_admin = super(IsAdminUserOrReadOnly, self).has_permission(
            request, view)
        # Python3: is_admin = super().has_permission(request, view)
        return request.method in SAFE_METHODS or is_admin
