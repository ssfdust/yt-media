#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    smorest_sfs.extensions.sqla.model
    ~~~~~~~~~~~~~~~~~~~~~~~~~~
    自定义Model模块
"""
from .softdelete import QueryWithSoftDelete
from .db_instance import db
from .mixin import CRUDMixin


class Model(CRUDMixin, db.Model):
    """简单的CRUD处理"""

    query_class = QueryWithSoftDelete

    __abstract__ = True
