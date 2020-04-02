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
"""
数据初始化模板
"""
from datetime import datetime
from getpass import getpass
from typing import Type

from smorest_sfs.modules.auth.permissions import \
    DEFAULT_ROLES_PERMISSIONS_MAPPING as mapping
from smorest_sfs.modules.auth.permissions import PERMISSIONS, ROLES
from smorest_sfs.modules.roles.models import Permission, Role
from smorest_sfs.modules.storages.models import Storages
from smorest_sfs.modules.users.models import Model, User, UserInfo, db


def create_item_from_cls(model_cls: Type[Model], cls: object) -> None:
    """根据类属性创建ORM"""
    names = [getattr(cls, attr) for attr in dir(cls) if not attr.startswith("__")]
    for name in names:
        model_cls(name=name).save()
    db.session.commit()


def _handle_default_role(role: Role) -> None:
    """hard code默认用户"""
    if role.name == ROLES.User:
        role.user_default = True


def init_permission() -> None:
    """根卷ROLES以及PERMISSION初始化权限"""
    create_item_from_cls(Role, ROLES)
    create_item_from_cls(Permission, PERMISSIONS)
    for role, permissions in mapping.items():
        permission_instances = Permission.query.filter(
            Permission.name.in_(permissions)
        ).all()
        role_instance = Role.query.filter_by(name=role).first()
        _handle_default_role(role_instance)
        role_instance.permissions = permission_instances
        db.session.add(role_instance)
    db.session.commit()


def init() -> None:
    """
    初始化数据
    """
    su_role = Role.get_by_name(name="SuperUser")
    password = getpass("Password:")

    # create super user
    root = User.create(
        username="wisdom",
        password=password,
        email="wisdom@zero.any.else",
        phonenum="1234567",
        active=True,
        confirmed_at=datetime.utcnow(),
    )
    avator = Storages(
        name="AdminAvator.jpg",
        storetype="avator",
        saved=True,
        filetype="image/jpeg",
        path="default/AdminAvator.jpg",
        uid=1,
    )
    UserInfo.create(user=root, avator=avator)
    root.roles.append(su_role)
    root.save()


def get_or_create(model_cls, name):
    item = model_cls.query.filter_by(name=name).first()
    if item:
        return item
    return model_cls(name=name).save(False)


def get_or_create_from_lst(model_cls, *names):
    lst = []
    for name in names:
        lst.append(get_or_create(model_cls, name))

    return lst


def update_permissions():
    """
    更新权限角色数据
    """
    for role_name, permissions in mapping.items():
        role = get_or_create(Role, role_name)
        permissions = get_or_create_from_lst(Permission, *permissions)
        role.add_permissions(permissions)

    db.session.commit()


def init_email_templates():
    """初始化邮件模板"""
    from smorest_sfs.modules.email_templates.models import EmailTemplate

    template = '<p>{{ message | safe }}</p><a href="{{ url }}" target="_blank">点击访问</a>'
    for name in ["default", "confirm", "reset-password"]:
        EmailTemplate.create(name=name, template=template)
