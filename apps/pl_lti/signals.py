#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  signals.py
#
#  Authors:
#       - Mamadou CISSE <mciissee.@gmail.com>
#

from django.dispatch import Signal

lti_request = Signal(providing_args=["request"])
