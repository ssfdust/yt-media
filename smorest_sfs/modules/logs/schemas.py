"""
    smorest_sfs.modules.logs.schemas
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    日志模块的Schemas
"""

from marshmallow import fields
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, auto_field

from smorest_sfs.extensions.marshal.bases import BasePageSchema, BaseParamSchema

from . import models


class LogParamSchema(SQLAlchemyAutoSchema, BaseParamSchema):
    """
    日志参数反序列化
    """

    module = auto_field(required=False)
    level = auto_field(required=False)

    class Meta:
        model = models.Log
        load_instance = False


class LogSchema(SQLAlchemyAutoSchema):
    """
    日志的序列化类
    """

    class Meta:
        model = models.Log


class LogPageSchema(BasePageSchema):
    """日志的分页"""

    data = fields.List(fields.Nested(LogSchema))
