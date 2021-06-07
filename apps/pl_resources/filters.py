#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  filters.py
#
#  Authors:
#       - Mamadou CISSE <mciissee.@gmail.com>
#
import datetime

from django.contrib.auth import get_user_model
from django.utils import timezone
from django_filters import rest_framework as filters

from .models import Circle, Resource

User = get_user_model()


class CircleFilter(filters.FilterSet):
    name = filters.CharFilter(label='Name', method='filter_name')
    member = filters.CharFilter(label='Member', method='filter_member')
    watcher = filters.CharFilter(label='Watcher', method='filter_watcher')

    updated_at = filters.NumberFilter(label='Updated at', method='filter_updated_at')

    class Meta:
        model = Circle
        fields = {
            'topics': ['exact'],
            'levels': ['exact'],
            'parent': ['exact'],
            'opened': ['exact']
        }

    def filter_name(self, queryset, name, value):
        return queryset.filter(name__icontains=value)

    def filter_member(self, queryset, name, value):
        user = User.objects.filter(username=value).first()
        if not user:
            return queryset.none()

        if user.is_admin:
            return queryset

        return queryset.filter(members__user__username=value)

    def filter_watcher(self, queryset, name, value):
        return queryset.filter(watchers__username=value)

    def filter_updated_at(self, queryset, name, value):
        if value == 0:
            return queryset
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
