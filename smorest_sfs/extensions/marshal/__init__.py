"""
    app.extensions.marshal
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~

    提供拓展的flask-marshmallow模块以更好地适应项目

    使用：
    >>> from app.extensions.marshal import ma
    >>> from flask import Flask
    >>> app = Flask('')
    >>> ma.init_app(app)
    >>> class SampleSchema(ma.Schema):
            id = fields.Int()
"""

from .bases import *
from .ma import Marshmallow, ModelSchema

ma = Marshmallow()
