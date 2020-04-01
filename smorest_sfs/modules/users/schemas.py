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
    app.modules.users.schemas
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    用户模块的Schemas
"""

from smorest_sfs.extensions import ma
from smorest_sfs.extensions.marshal.bases import BasePageSchema, BaseMsgSchema
from marshmallow import fields

from . import models


class UserSchema(ma.ModelSchema):
    """
    用户的序列化类
    """

    nickname = fields.Str(dump_only=True)

    class Meta:
        model = models.User


class UserSelfSchema(ma.ModelSchema):
    """
    用户的序列化类
    """

    nickname = fields.Str(dump_only=True)

    class Meta:
        model = models.User
        dump_only = ["roles", "active", "confirmed_at", "username"]


class UserPageSchema(BasePageSchema):
    """用户的分页"""

    data = fields.List(fields.Nested(UserSchema))


class UserItemSchema(BaseMsgSchema):
    """用户的单项"""

    data = fields.Nested(UserSchema)


class UserOptsSchema(ma.Schema):
    """用户的选项"""

    class Meta:
        fields = ("id", "nickname")


class UserListSchema(ma.Schema):
    """用户的选项列表"""

    data = fields.List(fields.Nested(UserOptsSchema))
