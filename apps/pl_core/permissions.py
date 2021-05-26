from rest_framework import permissions


class AdminOrTeacherPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if not bool(request.user and request.user.is_authenticated):
            return False
        return request.user.is_admin or request.user.is_editor


class AdminOrReadonlyPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        if not bool(request.user and request.user.is_authenticated):
            return False

        if request.method in permissions.SAFE_METHODS:
            return True

        if request.user.is_admin:
            return True

        return False
