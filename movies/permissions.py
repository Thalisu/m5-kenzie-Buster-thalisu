from rest_framework import permissions
from rest_framework.views import Request, View
from users.models import User


class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request: Request, view: View):
        if request.method in permissions.SAFE_METHODS:
            return True
        if type(request.user) is User:
            user = request.user
            return bool(user and (user.is_superuser or user.is_employee))
        return False
