from rest_framework import permissions
from rest_framework.permissions import IsAdminUser

class IsAdmin(permissions.BasePermission):

    def has_permission(self, request, view):
        return bool(
            request.user and (request.user.is_superuser)
        )
        
class IsStaff(IsAdminUser):
    def has_permission(self, request, view):
        return bool(request.user and (request.user.is_staff or request.user.is_superuser))
