#!/usr/bin/env python
# -*- coding: utf-8 -*-


from smorest_sfs.extensions.sqla import Model, SurrogatePK, db

from .users import Role

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

    def setup_roles(self) -> None:
        """
        设置默认组角色
        """
        if self.roles:
            return None

        roles = Role.query.filter_by(group_default=True).all()
        self.roles = roles

    def __str__(self) -> str:
        return self.name
