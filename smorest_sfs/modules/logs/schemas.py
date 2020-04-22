"""
    smorest_sfs.modules.logs.schemas
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    日志模块的Schemas
"""
from marshmallow import Schema, fields

from smorest_sfs.extensions.marshal import ModelSchema
from smorest_sfs.extensions.marshal.bases import BaseMsgSchema, BasePageSchema

from . import models


class LogSchema(ModelSchema):
    """
    日志的序列化类
    """

    class Meta:
        model = models.Log


class LogPageSchema(BasePageSchema):
    """日志的分页"""

    data = fields.List(fields.Nested(LogSchema))


class LogItemSchema(BaseMsgSchema):
    """日志的单项"""

    data = fields.Nested(LogSchema)


class LogOptsSchema(Schema):
    """日志的选项"""

    class Meta:
        fields = ("id", "name")


class LogListSchema(Schema):
    """日志的选项列表"""

    data = fields.List(fields.Nested(LogOptsSchema))
