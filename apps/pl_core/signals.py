#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  signals.py
#
#  Authors:
#       - Mamadou CISSE <mciissee.@gmail.com>
#

from django.dispatch import Signal

create_defaults = Signal(providing_args=["config"])
