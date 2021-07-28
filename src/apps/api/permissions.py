from rest_framework.permissions import BasePermission

from apps.users.models import UserRoles


class WriteEditDeletePermission(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.role >= UserRoles.READ_WRITE_EDIT_DELETE


class AdminPermission(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.role == UserRoles.ADMIN
