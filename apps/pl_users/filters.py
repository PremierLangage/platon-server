#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  filters.py
#
#  Authors:
#       - Mamadou CISSE <mciissee.@gmail.com>
#


from django.contrib.auth import get_user_model
from django_filters import rest_framework as filters
from django.db.models import Q

User = get_user_model()


class UserFilter(filters.FilterSet):
    is_admin = filters.BooleanFilter(label='Admin', method='filter_is_admin')

    class Meta:
        model = User
        fields = {
            'is_editor': ['exact']
        }

    def filter_is_admin(self, queryset, name, value):
        if value:
            return queryset.filter(
                Q(is_staff=True) | Q(is_superuser=True)
            )
        return queryset.filter(
            Q(is_staff=False) & Q(is_superuser=False)
        )
