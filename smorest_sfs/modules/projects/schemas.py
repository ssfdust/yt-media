#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright
# Author:
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
    smorest_sfs.modules.projects.schemas
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    项目模块的Schemas
"""

from smorest_sfs.extensions import ma
from smorest_sfs.extensions.marshal.bases import BasePageSchema, BaseMsgSchema
from marshmallow import fields

from . import models


class ProjectSchema(ma.ModelSchema):
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


class ProjectOptsSchema(ma.Schema):
    """项目的选项"""

    class Meta:
        fields = ("id", "name")


class ProjectListSchema(ma.Schema):
    """项目的选项列表"""

    data = fields.List(fields.Nested(ProjectOptsSchema))
