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
from typing import NoReturn
from sqlalchemy.orm.exc import NoResultFound
from smorest_sfs.modules.users.models import User, Role, Permission, UserInfo, db, Model
from smorest_sfs.modules.auth.permissions import (
    PERMISSIONS,
    ROLES,
    DEFAULT_ROLES_PERMISSIONS_MAPPING as mapping,
)

# from .modules.storages.models import Storages


def create_item_from_cls(model_cls: Model, cls: object) -> NoReturn:
    names = [getattr(cls, attr) for attr in dir(cls) if not attr.startswith("__")]
    for name in names:
        model_cls(name=name).save()
    db.session.commit()


def init_permission() -> NoReturn:
    create_item_from_cls(Role, ROLES)
    create_item_from_cls(Permission, PERMISSIONS)
    for role, permissions in mapping.items():
        permission_instances = Permission.query.filter(
            Permission.name.in_(permissions)
        ).all()
        role_instance = Role.query.filter_by(name=role).first()
        role_instance.permissions = permission_instances
        db.session.add(role_instance)
    db.session.commit()


def init():
    """
    初始化数据
    """
    su_role = Role.get_by_name(name="SuperUser")

    # create super user
    root = User.create(
        username="wisdom",
        password=encrypt_password("zerotoany"),
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


def update_permissions():
    """
    更新权限角色数据
    """
    for role_name, permissions in mapping.items():
        try:
            role = Role.query.filter_by(name=role_name).one()
        except NoResultFound:
            role = Role(name=role_name, description=role_name).save(False)

        for permission in permissions:
            try:
                permit = Permission.query.filter_by(name=permission).one()
            except NoResultFound:
                permit = Permission(name=permission, description=permission).save(False)
            if permit not in role.permissions:
                role.permissions.append(permit)

    db.session.commit()


def init_email_templates():
    """初始化邮件模板"""
    from app.modules.email_templates.models import EmailTemplate

    template = '<p>{{ message | safe }}</p><a href="{{ url }}" target="_blank">点击访问</a>'
    for name in ["default", "confirm", "reset-password"]:
        EmailTemplate.create(name=name, template=template)
