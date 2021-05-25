from rest_framework import permissions


class AdminOrTeacherPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if not bool(request.user and request.user.is_authenticated):
            return False
        profile = request.user.profile
        return profile.is_admin or profile.is_teacher


class AdminOrReadonlyPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        if not bool(request.user and request.user.is_authenticated):
            return False

        if request.method in permissions.SAFE_METHODS:
            return True

        profile = request.user.profile
        if profile.is_admin:
            return True

        return False
