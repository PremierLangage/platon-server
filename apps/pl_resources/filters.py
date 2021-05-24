#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  filters.py
#
#  Authors:
#       - Mamadou CISSE <mciissee.@gmail.com>
#
import datetime

from django.contrib.auth.models import User
from django.utils import timezone
from django_filters import rest_framework as filters

from .models import Circle, Resource


class CircleFilter(filters.FilterSet):
    member = filters.CharFilter(label='Member', method='filter_member')
    updated_at = filters.NumberFilter(label='Updated at', method='filter_updated_at')

    class Meta:
        model = Circle
        fields = {
            'name': ['iexact', 'icontains'],
            'topics': ['exact'],
            'levels': ['exact'],
            'parent': ['exact'],
        }

    def filter_member(self, queryset, name, value):
        user = User.objects.select_related('profile').filter(username=value).first()
        if not user:
            return queryset.none()

        if user.profile.is_admin:
            return queryset

        return queryset.filter(members__user__username=value)

    def filter_updated_at(self, queryset, name, value):
        date = timezone.now() - datetime.timedelta(days=int(value))
        return queryset.filter(updated_at__date__gte=date)


class ResourceFilter(filters.FilterSet):
    author = filters.CharFilter(label='Author', method='filter_author')
    updated_at = filters.NumberFilter(label='Updated at', method='filter_updated_at')

    class Meta:
        model = Resource
        fields = {
            'name': ['iexact', 'icontains'],
            'type': ['exact'],
            'topics': ['exact'],
            'levels': ['exact'],
            'circle': ['exact'],
        }

    def filter_author(self, queryset, name, value):
        return queryset.filter(author__username=value)

    def filter_updated_at(self, queryset, name, value):
        date = timezone.now() - datetime.timedelta(days=int(value))
        return queryset.filter(updated_at__date__gte=date)
