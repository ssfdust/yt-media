#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    smorest_sfs.extensions.sqla.model
    ~~~~~~~~~~~~~~~~~~~~~~~~~~
    自定义Model模块
"""
from flask_sqlalchemy.model import DefaultMeta

from .db_instance import db
from .mixin import CRUDMixin
from .softdelete import QueryWithSoftDelete

BaseModel: DefaultMeta = getattr(db, "Model")


class Model(BaseModel, CRUDMixin):
    """简单的CRUD处理"""

    query_class = QueryWithSoftDelete

    __abstract__ = True
