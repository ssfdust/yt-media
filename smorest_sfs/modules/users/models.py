#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
    smorest_sfs.modules.users.models
    ~~~~~~~~~~~~~~~~~~~~~~~~~

    用户的ORM模块
"""
from __future__ import annotations

from typing import TYPE_CHECKING

from marshmallow.validate import OneOf, Range
from sqlalchemy import Boolean, Column, DateTime, Integer, String, and_, join, or_
from sqlalchemy.orm import relationship
from sqlalchemy_utils.types import PasswordType

from smorest_sfs.extensions.sqla import Model, SurrogatePK, db
from smorest_sfs.modules.roles.models import permission_roles

if TYPE_CHECKING:
    from smorest_sfs.modules.roles.models import Role, Permission
    from smorest_sfs.modules.storages.models import Storages

roles_users = db.Table(
    "roles_users",
    Column("user_id", Integer(), nullable=False),
    Column("role_id", Integer(), nullable=False),
)


user_permissions = join(
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

    username = Column(String(255), nullable=False, unique=True, doc="用户名")
    phonenum = Column(String(255), nullable=True, unique=True, doc="电话号码")
    email = Column(String(255), nullable=True, unique=True, doc="用户邮箱")
    password = Column(
        PasswordType(schemes=["pbkdf2_sha512"]), nullable=False, doc="用户密码"
    )
    active = Column(Boolean(), doc="启用", default=False)
    confirmed_at = Column(DateTime(), doc="确认时间")
    roles = relationship(
        "Role",
        secondary=roles_users,
        uselist=True,
        doc="所有角色",
        primaryjoin="foreign(roles_users.c.user_id) == User.id",
        secondaryjoin="foreign(roles_users.c.role_id) == Role.id",
        backref=db.backref("users", lazy="dynamic", doc="所有用户"),
        info={"marshmallow": {"column": ["id", "name"]}},
    )
    permissions = relationship(
        "Permission",
        secondary=user_permissions,
        doc="权限",
        primaryjoin="User.id == roles_users.c.user_id",
        secondaryjoin="Permission.id == permission_roles.c.permission_id",
        backref=db.backref("users", doc="用户", lazy="dynamic"),
        viewonly=True,
        info={"marshmallow": {"dump_only": True, "column": ["id", "name"]}},
    )
    userinfo = relationship(
        "UserInfo",
        doc="用户",
        primaryjoin="User.id == UserInfo.uid",
        foreign_keys="UserInfo.uid",
        uselist=False,
        lazy="joined",
        info={
            "marshmallow": {
                "column": ["avator_id", "first_name", "last_name", "sex", "age"]
            }
        },
    )

    @classmethod
    def get_by_keyword(cls, keyword: str, raises: bool = False) -> User:
        """
        根据邮箱获取用户
        """
        user: User
        query = cls.query.filter(
            db.and_(
                or_(
                    cls.email == keyword,
                    cls.username == keyword,
                    cls.phonenum == keyword,
                ),
            )
        )
        if raises:
            user = query.one()
        user = query.first()
        return user

    def __str__(self) -> str:  # pragma: no cover
        if self.email:
            return self.email
        return ""

    @property
    def nickname(self) -> str:
        return self.userinfo.nickname


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

    avator_id = Column(Integer, doc="头像ID", info={"marshmallow": {"dump_only": True}})
    uid = Column(Integer, doc="用户ID", info={"marshmallow": {"dump_only": True}})
    avator = relationship(
        "Storages",
        primaryjoin="Storages.id == UserInfo.avator_id",
        foreign_keys=avator_id,
        doc="头像",
        lazy="joined",
        info={"marshmallow": {"dump_only": True}},
    )
    sex = Column(
        Integer,
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
    age = Column(
        Integer,
        doc="年龄",
        info={
            "marshmallow": {
                "allow_none": False,
                "validate": [Range(1, None)],
                "required": True,
            }
        },
    )
    first_name = Column(
        String(80),
        doc="姓",
        info={"marshmallow": {"allow_none": False, "required": True}},
    )
    last_name = Column(
        String(80),
        doc="名",
        info={"marshmallow": {"allow_none": False, "required": True}},
    )
    user = relationship(
        "User",
        doc="用户",
        primaryjoin="User.id == UserInfo.uid",
        foreign_keys=uid,
        info={"marshmallow": {"dump_only": True}},
    )

    def __str__(self) -> str:
        return self.user.username

    @property
    def nickname(self) -> str:
        if self.first_name and self.last_name:
            return self.first_name + " " + self.last_name
        return self.user.username

    @property
    def sex_label(self) -> str:
        """性别标签"""
        labels = {1: "男", 2: "女"}
        try:
            return labels[self.sex]
        except KeyError:
            return "未填写"
