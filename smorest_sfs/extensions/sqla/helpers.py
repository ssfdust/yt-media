#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
辅助函数模块
"""

from datetime import datetime
from sqlalchemy.sql import expression
from sqlalchemy.ext.compiler import compiles
from sqlalchemy.types import DateTime
from . import Model


def set_default_for_instance(instance: Model) -> Model:
    for key in ["modified", "created"]:
        setattr(instance, key, datetime.utcnow())
    setattr(instance, "deleted", False)
    return instance


class utcnow(expression.FunctionElement):
    # pylint: disable=R0901
    type = DateTime()


@compiles(utcnow, "postgresql")
def pg_utcnow(element, compiler, **kw) -> str:
    # pylint: disable=W0613
    return "TIMEZONE('utc', CURRENT_TIMESTAMP)"
