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
    MEMBER = 'MEMBER'


class EventTypes(models.TextChoices):
    MEMBER_CREATE = 'MEMBER_CREATE'
    MEMBER_REMOVE = 'MEMBER_REMOVE'

    RESOURCE_CREATE = 'RESOURCE_CREATE'
    RESOURCE_STATUS_CHANGE = 'RESOURCE_STATUS_CHANGE'


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
