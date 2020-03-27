#!/usr/bin/env python3
# -*- coding: utf-8 -*-
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
    app.modules.auth.models
    ~~~~~~~~~~~~~~~~~~~~~~~~~
    权限登录模块ORM
"""
from typing import Set, NoReturn
from marshmallow.validate import OneOf, Range
from sqlalchemy_utils.types import PasswordType
from smorest_sfs.extensions.sqla import Model, SurrogatePK, db
from smorest_sfs.modules.auth.permissions import ROLES

groups_users = db.Table(
    "groups_users",
    db.Column("group_id", db.Integer(), nullable=False),
    db.Column("user_id", db.Integer(), nullable=False),
)

groups_roles = db.Table(
    "groups_roles",
    db.Column("group_id", db.Integer(), nullable=False),
    db.Column("role_id", db.Integer(), nullable=False),
)

groups_relation = db.Table(
    "groups_relation",
    db.Column("ancestor", db.Integer(), nullable=False),
    db.Column("descendant", db.Integer(), nullable=False),
    db.Column("distance", db.Integer(), nullable=False),
)

permission_roles = db.Table(
    "permission_roles",
    db.Column("permission_id", db.Integer(), nullable=False),
    db.Column("role_id", db.Integer(), nullable=False),
)

roles_users = db.Table(
    "roles_users",
    db.Column("user_id", db.Integer(), nullable=False),
    db.Column("role_id", db.Integer(), nullable=False),
)


class Permission(Model, SurrogatePK):
    """
    角色表

    :attr name: str(80) 权限名称
    :attr description: str(255) 权限描述
    :attr roles: Role 所有角色
    :attr users: User 所有用户
    """

    __tablename__ = "permissions"

    name = db.Column(db.String(80), unique=True, doc="权限名称", nullable=True)
    description = db.Column(db.String(255), doc="权限描述")

    @classmethod
    def get_by_name(cls, name: str) -> Model:  # pragma: no cover
        return cls.query.filter_by(name=name).first()

    def __str__(self) -> str:  # pragma: no cover
        return self.name


class Role(Model, SurrogatePK):
    """
    角色表

    :attr name: str(80) 角色名称
    :attr description: str(255) 角色描述
    :attr permissions: Permission 所有权限
    :attr user_default: bool 用户默认角色
    :attr group_default: bool 组默认角色
    """

    __tablename__ = "roles"

    name = db.Column(db.String(80), unique=True, doc="角色名称", nullable=True)
    description = db.Column(db.String(255), doc="角色描述")
    user_default = db.Column(db.Boolean, doc="用户默认角色", default=False)
    group_default = db.Column(db.Boolean, doc="组默认角色", default=False)
    permissions = db.relationship(
        "Permission",
        secondary=permission_roles,
        doc="所有权限",
        primaryjoin="foreign(permission_roles.c.role_id) == Role.id",
        secondaryjoin="foreign(permission_roles.c.permission_id) == Permission.id",
        backref=db.backref("roles", lazy="dynamic", doc="所有角色"),
    )

    @classmethod
    def get_by_name(cls, name: str) -> Model:  # pragma: no cover
        return cls.query.filter_by(name=name).first()

    @classmethod
    def get_by_user_default(cls, is_admin=False) -> Model:  # pragma: no cover
        if is_admin:
            return cls.query.filter_by(ROLES.SuperUser).all()
        return cls.query.filter_by(user_default=True).all()  # pragam: no cover

    def get_permissions(self) -> Set[Permission]:  # pragma: no cover
        """
        获取权限

        兼容flask-security
        """
        return set(permission.name for permission in self.permissions)

    def __str__(self) -> str:  # pragma: no cover
        return self.name


user_permissions = db.join(
    roles_users, permission_roles, roles_users.c.role_id == permission_roles.c.role_id
)


class User(Model, SurrogatePK):
    """
    用户表

    :attr username: str(255) 用户名
    :attr email: str(255) 用户邮箱
    :attr password: str(255) 用户密码
    :attr active: bool 是否启用
    :attr confirmed_at: DateTime 确认时间
    :attr roles: Role 角色
    :attr permissions: Permission 权限
    """

    __tablename__ = "users"

    username = db.Column(db.String(255), nullable=False, unique=True, doc="用户名")
    phonenum = db.Column(db.String(255), nullable=True, unique=True, doc="电话号码")
    email = db.Column(db.String(255), nullable=True, unique=True, doc="用户邮箱")
    password = db.Column(
        PasswordType(schemes=["pbkdf2_sha512"]), nullable=False, doc="用户密码"
    )
    active = db.Column(db.Boolean(), doc="启用", default=False)
    confirmed_at = db.Column(db.DateTime(), doc="确认时间")
    roles = db.relationship(
        "Role",
        secondary=roles_users,
        doc="所有角色",
        primaryjoin="foreign(roles_users.c.user_id) == User.id",
        secondaryjoin="foreign(roles_users.c.role_id) == Role.id",
        backref=db.backref("users", lazy="dynamic", doc="所有用户"),
        info={"marshmallow": {"dump_only": True, "column": ["id", "name"]}},
    )
    permissions = db.relationship(
        "Permission",
        secondary=user_permissions,
        doc="权限",
        primaryjoin="User.id == roles_users.c.user_id",
        secondaryjoin="Permission.id == permission_roles.c.permission_id",
        backref=db.backref("users", doc="用户", lazy="dynamic"),
        viewonly=True,
        info={"marshmallow": {"dump_only": True, "column": ["id", "name"]}},
    )

    @classmethod
    def get_by_keyword(cls, keyword: str) -> Model:
        """
        根据邮箱获取用户
        """
        return cls.query.filter(
            db.and_(
                cls.deleted.is_(False),
                db.or_(
                    cls.email == keyword,
                    cls.username == keyword,
                    cls.phonenum == keyword,
                ),
            )
        ).first()

    def __str__(self) -> str:  # pragma: no cover
        return self.email

    @property
    def nickname(self) -> str:
        if self.userinfo.first_name and self.userinfo.last_name:
            return self.userinfo.first_name + self.userinfo.last_name
        return self.username


class Group(Model, SurrogatePK):
    """
    组别表

    :attr name: str(80) 组名称
    :attr description: str(255) 组描述
    :attr pid: int 父组ID
    :attr roles: Role 组默认角色
    :attr users: User 组成员
    :attr parent: Group 父组
    :attr children: Group 子组
    """

    __tablename__ = "groups"

    name = db.Column(db.String(80), unique=True, doc="组名称", nullable=True)
    description = db.Column(db.String(255), doc="组描述")
    pid = db.Column(db.Integer(), doc="父组ID")
    users = db.relationship(
        "User",
        secondary="groups_users",
        primaryjoin="Group.id == groups_users.c.group_id",
        secondaryjoin="User.id == groups_users.c.user_id",
        doc="组下用户",
        foreign_keys="[groups_users.c.group_id," "groups_users.c.user_id]",
        backref=db.backref("groups", lazy="dynamic", doc="所有组"),
        active_history=True,
        lazy="joined",
    )
    roles = db.relationship(
        "Role",
        secondary="groups_roles",
        primaryjoin="Group.id == groups_roles.c.group_id",
        secondaryjoin="Role.id == groups_roles.c.role_id",
        doc="组下默认角色",
        foreign_keys="[groups_roles.c.group_id," "groups_roles.c.role_id]",
        backref=db.backref("groups", lazy="dynamic", doc="所属组"),
        cascade="all,delete",
        active_history=True,
        lazy="joined",
    )
    parent = db.relationship(
        "Group",
        primaryjoin="remote(Group.id) == Group.pid",
        foreign_keys=pid,
        doc="父节点",
        info={"marshmallow": {"dump_only": True}},
    )
    children = db.relationship(
        "Group",
        secondary="groups_relation",
        primaryjoin="Group.id == groups_relation.c.ancestor",
        doc="子组别",
        secondaryjoin=(
            "and_(Group.id == groups_relation.c.descendant,"
            "groups_relation.c.distance > 0)"
        ),
        viewonly=True,
    )

    @classmethod
    def get_by_name(cls, name: str) -> Model:
        return cls.query.filter_by(name=name).first()

    def setup_roles(self) -> NoReturn:
        """
        设置默认组角色
        """
        if self.roles:
            return

        roles = Role.query.filter_by(group_default=True).all()
        self.roles = roles

    def __str__(self) -> str:
        return self.name


class UserInfo(SurrogatePK, Model):
    """
    用户信息表

    :attr avator_id: int 用户头像ID
    :attr uid: int 用户ID
    :attr avator: Storages 用户头像
    :attr user: User 关联用户
    :attr sex: int 性别
    :attr age: int 年龄
    :attr first_name: str(80) 姓
    :attr second_name: str(80) 名
    """

    # from app.modules.storages.models import Storages

    __tablename__ = "userinfo"

    avator_id = db.Column(
        db.Integer, doc="头像ID", info={"marshmallow": {"dump_only": True}}
    )
    uid = db.Column(db.Integer, doc="用户ID", info={"marshmallow": {"dump_only": True}})
    #  avator = db.relationship(
    #      "Storages",
    #      primaryjoin="Storages.id == UserInfo.avator_id",
    #      foreign_keys=avator_id,
    #      doc="头像",
    #      lazy="joined",
    #      info={"marshmallow": {"dump_only": True}},
    #  )
    sex = db.Column(
        db.Integer,
        doc="性别",
        default=1,
        info={
            "marshmallow": {
                "validate": [OneOf([1, 2])],
                "allow_none": False,
                "required": True,
            }
        },
    )
    age = db.Column(
        db.Integer,
        doc="年龄",
        info={
            "marshmallow": {
                "allow_none": False,
                "validate": [Range(1, None)],
                "required": True,
            }
        },
    )
    first_name = db.Column(
        db.String(80),
        doc="姓",
        info={"marshmallow": {"allow_none": False, "required": True}},
    )
    last_name = db.Column(
        db.String(80),
        doc="名",
        info={"marshmallow": {"allow_none": False, "required": True}},
    )
    user = db.relationship(
        "User",
        doc="用户",
        primaryjoin="User.id == UserInfo.uid",
        foreign_keys=uid,
        backref=db.backref(
            "userinfo",
            uselist=False,
            lazy="joined",
            info={"marshmallow": {"column": ["avator_id"]}},
        ),
        info={"marshmallow": {"dump_only": True}},
    )

    def __str__(self) -> str:
        return self.user.username

    @property
    def sex_label(self) -> str:
        """性别标签"""
        labels = {1: "男", 2: "女"}
        try:
            return labels[self.sex]
        except KeyError:
            return "未填写"
