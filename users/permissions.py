from rest_framework import permissions
from rest_framework.views import Request, View
from users.models import User


class IsEmployeeOrSameUser(permissions.BasePermission):
    def has_permission(self, request: Request, view: View, c_user: User):
        if type(request.user) is User:
            user = request.user
            return bool(
                user.is_superuser or user.is_employee or c_user == request.user
            )
        return False
