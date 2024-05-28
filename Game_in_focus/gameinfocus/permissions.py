from rest_framework.permissions import BasePermission
from django.contrib.auth import get_user


class IsAuthenticated(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated)