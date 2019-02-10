from rest_framework import permissions
 
class isOwnerOrAdmin(permissions.BasePermission):
    """This class creates permissions for delete and update methods"""

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user or request.user.is_staff