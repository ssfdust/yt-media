#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
自定义错误类型
"""
from psycopg2.errors import UniqueViolation, StringDataRightTruncation
from .db_instance import db


class DuplicateEntry(Exception):
    """重复的类型"""


class CharsTooLong(Exception):
    """字符过长"""


err_mapping = {
    UniqueViolation: DuplicateEntry,
    StringDataRightTruncation: CharsTooLong,
}


def pgerr_to_customerr(err):
    for err_cls, custom_err_cls in err_mapping.items():
        if isinstance(err.orig, err_cls):
            db.session.rollback()
            raise custom_err_cls(str(err))
