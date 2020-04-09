#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright 2019 ssfdust RedLotus
# Author: ssfdust RedLotus
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
    smorest_sfs.modules.email_templates.schemas
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    电子邮件模板模块的Schemas
"""

from marshmallow import Schema, fields

from smorest_sfs.extensions.marshal import ModelSchema
from smorest_sfs.extensions.marshal.bases import BaseMsgSchema, BasePageSchema

from . import models


class EmailTemplateSchema(ModelSchema):
    """
    电子邮件模板的序列化类
    """

    class Meta:
        model = models.EmailTemplate


class EmailTemplatePageSchema(BasePageSchema):
    """电子邮件模板的分页"""

    data = fields.List(fields.Nested(EmailTemplateSchema))


class EmailTemplateItemSchema(BaseMsgSchema):
    """电子邮件模板的单项"""

    data = fields.Nested(EmailTemplateSchema)


class EmailTemplateOptsSchema(Schema):
    """电子邮件模板的选项"""

    class Meta:
        fields = ("id", "name")


class EmailTemplateListSchema(Schema):
    """电子邮件模板的选项列表"""

    data = fields.List(fields.Nested(EmailTemplateOptsSchema))
