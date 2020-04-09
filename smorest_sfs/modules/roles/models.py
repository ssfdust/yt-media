#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
    smorest_sfs.modules.roles.models
    ~~~~~~~~~~~~~~~~~~~~~~~~~

    角色权限的ORM模块
"""
from __future__ import annotations

from typing import List

from sqlalchemy import Boolean, Column, String
from sqlalchemy.orm import relationship

from smorest_sfs.extensions.sqla import Model, SurrogatePK, db
from smorest_sfs.modules.auth.permissions import ROLES

permission_roles = db.Table(
    "permission_roles",
    db.Column("permission_id", db.Integer(), nullable=False),
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

    name = Column(String(80), unique=True, doc="权限名称", nullable=False)
    description = Column(String(255), doc="权限描述")

    @classmethod
    def get_by_name(cls, name: str) -> Permission:
        permission: Permission = cls.query.filter_by(name=name).first()
        return permission

    @classmethod
    def get_by_names(cls, *names: List[str]) -> List[Permission]:
        permissions: List[Permission] = cls.query.filter(cls.name.in_(names)).all()
        return permissions

    def __str__(self) -> str:
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

    name = Column(String(80), unique=True, doc="角色名称", nullable=False)
    description = Column(String(255), doc="角色描述")
    user_default = Column(Boolean, doc="用户默认角色", default=False)
    group_default = Column(Boolean, doc="组默认角色", default=False)
    permissions = relationship(
        "Permission",
        secondary=permission_roles,
        doc="所有权限",
        primaryjoin="foreign(permission_roles.c.role_id) == Role.id",
        secondaryjoin="foreign(permission_roles.c.permission_id) == Permission.id",
        backref=db.backref("roles", lazy="dynamic", doc="所有角色"),
        info={"marshmallow": {"column": ["id", "name"]}},
    )

    @classmethod
    def get_by_name(cls, name: str) -> Role:
        role: Role = cls.query.filter_by(name=name).first()
        return role

    @classmethod
    def get_by_user_default(cls, is_admin: bool = False) -> List[Role]:
        roles: List[Role]
        if is_admin:
            roles = cls.query.filter_by(name=ROLES.SuperUser).all()
        else:
            roles = cls.query.filter_by(user_default=True).all()
        return roles

    def add_permissions(self, permissions: List[Permission]) -> List[Permission]:
        """
        获取权限

        兼容flask-security
        """
        for permission in permissions:
            if permission not in self.permissions:
                self.permissions.append(permission)
        return list(permission.name for permission in self.permissions)

    def __str__(self) -> str:
        return self.name
