# Copyright 2019 RedLotus <ssfdust@gmail.com>
# Author: RedLotus <ssfdust@gmail.com>
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

from typing import List, Dict
from marshmallow import fields, post_load

from smorest_sfs.extensions import ma
from smorest_sfs.extensions.marshal.bases import BaseMsgSchema

from . import models


class UserInfoSchema(ma.ModelSchema):
    class Meta:
        model = models.UserInfo


class UserSchema(ma.ModelSchema):

    session = models.db.session

    userinfo = fields.Nested(UserInfoSchema)

    class Meta:

        model = models.User


class UserDetailsSchema(BaseMsgSchema):

    data = fields.Nested(UserSchema)


class GroupSchema(ma.ModelSchema):
    """
    组
    """

    children = fields.List(fields.Nested("self"), dump_only=True)

    class Meta:
        model = models.Group


class GroupItemSchema(BaseMsgSchema):
    """
    组返回
    """

    data = fields.Nested(GroupSchema)


class GroupResSchema(BaseMsgSchema):

    data = fields.List(fields.Nested(GroupSchema))


class UserListByIdParam(ma.Schema):
    """
    处理形如
    {'users': [1, 2, 3, 4]}
    json格式
    """

    users = fields.List(fields.Int, description="用户ID列表")

    @post_load
    def load_users(self, data: Dict[str, List[int]]) -> List[models.User]:
        users = models.User.query.filter(
            models.User.id.in_(data["users"])
        ).all()

        return users
