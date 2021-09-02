#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  permissions.py
#
#  Authors:
#       - Mamadou CISSE <mciissee.@gmail.com>
#

from django.contrib.auth import get_user_model
from rest_framework import permissions
from rest_framework.request import Request
from rest_framework.viewsets import ViewSetMixin

from .models import Circle, Member, Resource

User = get_user_model()


class CirclePermission(permissions.BasePermission):
    def has_permission(self,  request: Request, view: ViewSetMixin):
        if not bool(request.user and request.user.is_authenticated):
            return False

        if request.user.is_admin:
            return True

        if not request.user.is_editor:
            return False

        if request.method in permissions.SAFE_METHODS:
            return True

        if request.method == 'POST':
            return request.user.is_admin

        return True

    def has_object_permission(self, request: Request, view: ViewSetMixin, obj: Circle):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_admin


class EventPermission(permissions.BasePermission):
    def has_permission(self,  request: Request, view: ViewSetMixin):
        if not bool(request.user and request.user.is_authenticated):
            return False

        if request.user.is_admin:
            return True

        if not request.user.is_editor:
            return False

        if request.method in permissions.SAFE_METHODS:
            return True

        return request.user.is_admin


class MemberPermission(permissions.BasePermission):
    def has_permission(self,  request: Request, view: ViewSetMixin):
        if not bool(request.user and request.user.is_authenticated):
            return False

        if request.user.is_admin:
            return True

        if not request.user.is_editor:
            return False

        if request.method in permissions.SAFE_METHODS:
            return True

        if request.user.username == view.kwargs.get("username"):
            return True

        return request.user.is_admin


class ResourcePermission(permissions.BasePermission):
    def has_permission(self, request: Request, view: ViewSetMixin):
        if not bool(request.user and request.user.is_authenticated):
            return False

        if request.user.is_admin:
            return True

        if not request.user.is_editor:
            return False

        if request.method in permissions.SAFE_METHODS:
            return True

        if view.action == "create":
            circle = Circle.objects.get(request.data.get("circle"))
            return circle.opened or Circle.is_member(request.user, circle.id)

        return True

    def has_object_permission(self, request: Request, view: ViewSetMixin, obj: Resource):
        if view.action == "destroy" and not obj.is_deletable_by(request.user):
            return False

        if view.action == "partial_update" and not obj.is_editable_by(request.user):
            return False

        return True


class FilePermission(permissions.BasePermission):

    def has_permission(self, request: Request, view: ViewSetMixin):
        if request.method in permissions.SAFE_METHODS:
            return True

        if not bool(request.user and request.user.is_authenticated):
            return False

        if request.query_params.get('version', 'master') != 'master':
            self.message = 'Cannot update versioned file'
            return False

        undeletable_paths = ['', '.', 'resource-info.json']
        path = view.kwargs.get('path').strip()
        if request.method == 'DELETE' and path in undeletable_paths:
            self.message = f'Cannot delete "{path}"'
            return False

        if not request.user.is_editor:
            return False

        if request.user.is_admin:
            return True

        type, id = view.kwargs.get('directory').split(':')
        if type == 'resource':
            resource = Resource.objects.filter(pk=int(id)).first()
            if not resource:
                return False
            return resource.is_editable_by(request.user)

        circle = Circle.objects.filter(pk=int(id)).first()
        if not circle:
            return False

        return Circle.is_member(request.user, id)
