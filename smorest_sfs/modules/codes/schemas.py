"""
    smorest_sfs.modules.codes.schemas
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    编码模块的Schemas
"""
from marshmallow import Schema, fields

from smorest_sfs.extensions.marshal import ModelSchema
from smorest_sfs.extensions.marshal.bases import BaseMsgSchema, BasePageSchema

from . import models


class CodeSchema(ModelSchema):
    """
    编码的序列化类
    """

    class Meta:
        model = models.Code


class CodePageSchema(BasePageSchema):
    """编码的分页"""

    data = fields.List(fields.Nested(CodeSchema))


class CodeItemSchema(BaseMsgSchema):
    """编码的单项"""

    data = fields.Nested(CodeSchema)


class CodeOptsSchema(Schema):
    """编码的选项"""

    class Meta:
        fields = ("id", "name", "type_code")


class CodeListSchema(Schema):
    """编码的选项列表"""

    data = fields.List(fields.Nested(CodeOptsSchema))
