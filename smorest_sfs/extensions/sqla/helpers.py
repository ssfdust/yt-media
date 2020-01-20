#!/usr/bin/env python
# -*- coding: utf-8 -*-


from datetime import datetime


def set_default_for_instance(instance):
    for key in ["modified", "created"]:
        setattr(instance, key, datetime.utcnow())
    setattr(instance, "deleted", False)
    return instance
