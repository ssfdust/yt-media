"""
    smorest_sfs.modules.projects.schemas
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    项目模块的Schemas
"""
from marshmallow import Schema, fields

from smorest_sfs.extensions.marshal import ModelSchema
from smorest_sfs.extensions.marshal.bases import BaseMsgSchema, BasePageSchema

from . import models


class ProjectSchema(ModelSchema):
    """
    项目的序列化类
    """

    class Meta:
        model = models.Project


class ProjectPageSchema(BasePageSchema):
    """项目的分页"""

    data = fields.List(fields.Nested(ProjectSchema))


class ProjectItemSchema(BaseMsgSchema):
    """项目的单项"""

    data = fields.Nested(ProjectSchema)


class ProjectOptsSchema(Schema):
    """项目的选项"""

    class Meta:
        fields = ("id", "name")


class ProjectListSchema(Schema):
    """项目的选项列表"""

    data = fields.List(fields.Nested(ProjectOptsSchema))
