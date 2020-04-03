"""
    app.extensions.marshal.ma
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Marshmallow拓展模块

    为所有的ModelSchema类，默认unknown为EXCLUDE，因为项目中所有接口都会返回
    id, deleted, created, modified这四个属性，并不允许从前端提交，所以默认为
    EXCLUDE而不是RAISE。否则前端需要对递归属性进行除重。
"""
from typing import Any, Optional

from flask import Flask
from flask_marshmallow import Marshmallow as BaseMarshmallow
from flask_marshmallow import sqla
from marshmallow import EXCLUDE, Schema


class SchemaOpts(sqla.SchemaOpts):
    """Schema options

    继承flask_marshmallow的opts，在其基础上再次添加unknown属性，
    以及自定义的ModelConverter。
    """

    def __init__(self, meta: Schema.Meta, **kwargs: Any):
        if not hasattr(meta, "unknown"):
            meta.unknown = EXCLUDE
        super(SchemaOpts, self).__init__(meta, **kwargs)


class ModelSchema(sqla.ModelSchema):
    """
    为ModelSchema替换新的SchemaOpts类
    """

    OPTIONS_CLASS = SchemaOpts


class Marshmallow(BaseMarshmallow):
    """
    用新的ModelSchema替换旧有的，已添加支持
    """

    def __init__(self, app: Optional[Flask] = None):
        super().__init__(app)
        self.ModelSchema = ModelSchema
