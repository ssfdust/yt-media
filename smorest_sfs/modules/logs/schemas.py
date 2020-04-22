"""
    smorest_sfs.modules.logs.schemas
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    日志模块的Schemas
"""
from marshmallow import fields
from marshmallow_sqlalchemy import SQLAlchemySchema, auto_field

from smorest_sfs.extensions.marshal.bases import BasePageSchema

from . import models


class LogSchema(SQLAlchemySchema):
    """
    日志的序列化类
    """

    class Meta:
        model = models.Log
        load_instance = False

    gt__created = auto_field("created", load_only=True, dump_only=False)


class LogPageSchema(BasePageSchema):
    """日志的分页"""

    data = fields.List(fields.Nested(LogSchema))
