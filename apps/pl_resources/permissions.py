#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  permissions.py
#
#  Authors:
#       - Mamadou CISSE <mciissee.@gmail.com>
#

from django.contrib.auth.models import User
from rest_framework import permissions
from rest_framework.request import Request
from rest_framework.viewsets import ViewSetMixin

from .enums import CircleTypes, MemberStatus
from .models import Circle, Member, Resource


def is_circle_owner(user: User, circle_id: str) -> bool:
    member = Member.objects.filter(
        user_id=user.id,
        circle_id=circle_id,
    ).first()
    return member and member.status == MemberStatus.OWNER


def is_circle_member(user: User, circle_id: str) -> bool:
    return Member.objects.filter(
        user_id=user.id,
        circle_id=circle_id,
    ).exists()


class CirclePermission(permissions.BasePermission):
    def has_permission(self,  request: Request, view: ViewSetMixin):
        if not bool(request.user and request.user.is_authenticated):
            return False

        profile = request.user.profile
        if not profile.is_teacher:
            return False

        if profile.is_admin:
            return True

        if request.method in permissions.SAFE_METHODS:
            return True

        if request.method == 'POST':
            return profile.is_admin

        return True

    def has_object_permission(self, request: Request, view: ViewSetMixin, obj: Circle):
        if request.method in permissions.SAFE_METHODS:
            return True

        profile = request.user.profile
        if request.method == 'DELETE':
            if obj.type == CircleTypes.PERSONAL:
                return False
            return profile.is_admin

        return profile.is_admin or is_circle_owner(request.user, obj.pk)


class EventPermission(permissions.BasePermission):
    def has_permission(self,  request: Request, view: ViewSetMixin):
        if not bool(request.user and request.user.is_authenticated):
            return False

        profile = request.user.profile
        if not profile.is_teacher:
            return False

        if profile.is_admin:
            return True

        if request.method in permissions.SAFE_METHODS:
            return True

        return is_circle_owner(request.user, view.kwargs.get("circle_id"))


class MemberPermission(permissions.BasePermission):
    def has_permission(self,  request: Request, view: ViewSetMixin):
        if not bool(request.user and request.user.is_authenticated):
            return False

        profile = request.user.profile
        if not profile.is_teacher:
            return False

        if profile.is_admin:
            return True

        if request.method in permissions.SAFE_METHODS:
            return True

        if request.user.username == view.kwargs.get("username"):
            return True

        return is_circle_owner(request.user, view.kwargs.get("circle_id"))


class WatcherPermission(MemberPermission):
    pass


class ResourcePermission(permissions.BasePermission):
    def has_permission(self, request: Request, view: ViewSetMixin):
        if not bool(request.user and request.user.is_authenticated):
            return False

        profile = request.user.profile
        if not profile.is_teacher:
            return False

        if profile.is_admin:
            return True

        if request.method in permissions.SAFE_METHODS:
            return True

        if view.action == "create":
            return is_circle_member(request.user, request.data.get("circle"))

        return True

    def has_object_permission(self, request: Request, view: ViewSetMixin, obj: Resource):
        if view.action == "partial_update" and not obj.is_editable_by(request.user):
            return False

        if view.action == "destroy":
            if obj.versions_count:
                self.message = "This resource is published"
                return False
            if not obj.is_deletable_by(request.user):
                return False

        return True


class VersionPermission(permissions.BasePermission):
    def __init__(self, resource: Resource):
        self.resource = resource

    def has_permission(self,  request: Request, view: ViewSetMixin):
        if request.method in ['DELETE', 'PUT']:
            return False

        if not bool(request.user and request.user.is_authenticated):
            return False

        if not request.user.profile.is_teacher:
            return False

        editable = self.resource.is_editable_by(request.user)
        return editable or request.method in permissions.SAFE_METHODS


class FilePermission(permissions.BasePermission):
    def __init__(self, resource: Resource):
        self.resource = resource

    def has_permission(self, request: Request, view: ViewSetMixin):
        if request.method in permissions.SAFE_METHODS:
            return True

        if view.kwargs.get('version'):
            self.message = 'Cannot update versions'
            return False

        undeletable_paths = ['', 'resource-info.json']
        path = view.kwargs.get('path').strip()
        if request.method == 'DELETE' and path in undeletable_paths:
            self.message = f'Cannot delete "{path}"'
            return False

        profile = request.user.profile
        if not profile.is_teacher:
            return False

        if profile.is_admin:
            return True

        return self.resource.is_editable_by(request.user)
