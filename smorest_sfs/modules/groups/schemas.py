"""
    smorest_sfs.modules.groups.schemas
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    用户组模块的Schemas
"""
from smorest_sfs.extensions.marshal import BasePageSchema, BaseMsgSchema, SQLAlchemyAutoSchema
from marshmallow import fields, Schema

from . import models


class GroupSchema(SQLAlchemyAutoSchema):
    """
    用户组的序列化类
    """

    class Meta:
        model = models.Group
        exclude = ['left', 'right']


class GroupPageSchema(BasePageSchema):
    """用户组的分页"""

    data = fields.List(fields.Nested(GroupSchema))


class GroupItemSchema(BaseMsgSchema):
    """用户组的单项"""

    data = fields.Nested(GroupSchema)


class GroupOptsSchema(Schema):
    """用户组的选项"""

    class Meta:
        fields = ('id', 'name')


class GroupListSchema(Schema):
    """用户组的选项列表"""

    data = fields.List(fields.Nested(GroupOptsSchema))
