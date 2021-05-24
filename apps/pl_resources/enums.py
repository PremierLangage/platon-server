#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  enums.py
#
#  Authors:
#       - Mamadou CISSE <mciissee.@gmail.com>
#

from django.db import models


class MemberStatus(models.TextChoices):
    OWNER = 'OWNER'
    MEMBER = 'MEMBER'


class CircleTypes(models.TextChoices):
    PUBLIC = 'PUBLIC'
    PERSONAL = 'PERSONAL'


class EventTypes(models.TextChoices):
    GENERIC = 'GENERIC'
    MEMBER_ADDED = 'MEMBER_ADDED'
    MEMBER_REMOVED = 'MEMBER_REMOVED'

    RESOURCE_CREATED = 'RESOURCE_CREATED'
    RESOURCE_UPDATED = 'RESOURCE_UPDATED'


class ResourceTypes(models.TextChoices):
    MODEL = 'MODEL'
    ACTIVITY = 'ACTIVITY'
    EXERCISE = 'EXERCISE'


class ResourceStatus(models.TextChoices):
    DRAFT = 'DRAFT'
    READY = 'READY'
    DEPRECATED = 'DEPRECATED'
    BUGGED = 'BUGGED'
    NOT_TESTED = 'NOT_TESTED'
