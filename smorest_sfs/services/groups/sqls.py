#!/usr/bin/env python
# -*- coding: utf-8 -*-
from typing import List, Tuple

from sqlalchemy import select, literal_column
from sqlalchemy.sql import Join

from smorest_sfs.extensions import db
from smorest_sfs.modules.groups.models import groups_roles
from smorest_sfs.modules.users.models import Group, User, groups_users, roles_users
from smorest_sfs.plugins.sa import SAStatement


class DeleteGroupFromUser(SAStatement):
    def __init__(self, user: User, groups: List[Group]):
        # pylint: disable=W0231
        self._groups = groups
        self._group_ids = [g.id for g in self._groups]
        self._user = user
        self._build_sql()

    def _build_sql(self) -> None:
        user_role = db.alias(self._get_user_role_sql(), "user_role")
        self.sa_sql = roles_users.delete().where(
            db.and_(
                roles_users.c.role_id == user_role.c.role_id,
                roles_users.c.user_id == user_role.c.user_id,
            )
        )

    def __get_group_user_role_sql(self) -> select:
        return db.alias(
            db.select(
                [
                    groups_roles.c.group_id,
                    groups_users.c.user_id,
                    groups_roles.c.role_id,
                ]
            )
            .select_from(
                db.join(
                    groups_roles,
                    groups_users,
                    groups_users.c.group_id == groups_roles.c.group_id,
                )
            )
            .where(groups_users.c.user_id == self._user.id),
            "group_user_role",
        )

    def __get_role_sql_tuple(self) -> Tuple[select, select, Join]:
        group_user_role = self.__get_group_user_role_sql()
        remaining_role_sql = db.alias(
            db.select([group_user_role.c.role_id]).where(
                group_user_role.c.group_id.notin_(self._group_ids)
            ),
            "remaining_role_sql",
        )
        deleted_role_sql = db.alias(
            db.select([group_user_role.c.role_id]).where(
                group_user_role.c.group_id.in_(self._group_ids)
            ),
            "deleted_role_sql",
        )
        joined_role_sql = deleted_role_sql.outerjoin(
            remaining_role_sql,
            remaining_role_sql.c.role_id == deleted_role_sql.c.role_id,
        )
        return (remaining_role_sql, deleted_role_sql, joined_role_sql)

    def _get_user_role_sql(self) -> select:
        remaining_role_sql, deleted_role_sql, joined_role_sql = self.__get_role_sql_tuple()
        return db.select(
            [
                deleted_role_sql.c.role_id,
                remaining_role_sql.c.role_id.label("r_role_id"),
                literal_column(str(self._user.id), db.Integer).label("user_id")
            ]
        ).select_from(joined_role_sql).where(remaining_role_sql.c.role_id.is_(None))


class AddUserToGroup(SAStatement):
    def __init__(self, user: User, groups: List[Group]):
        # pylint: disable=W0231
        self._groups = groups
        self._user = user
        self._build_sql()

    def _build_sql(self) -> None:
        absent_user_roles = self._get_absent_user_roles()
        self.sa_sql = roles_users.insert().from_select(
            ["user_id", "role_id"], absent_user_roles
        )

    def _get_absent_user_roles(self) -> select:
        roles_user = db.alias(
            db.select([roles_users]).where(roles_users.c.user_id == self._user.id),
            "roles_user",
        )
        joined_groups_user = db.outerjoin(
            groups_roles, roles_user, groups_roles.c.role_id == roles_user.c.role_id
        )
        return (
            db.select(
                [
                    db.func.coalesce(roles_user.c.user_id, self._user.id).label(
                        "user_id"
                    ),
                    groups_roles.c.role_id,
                ]
            )
            .select_from(joined_groups_user)
            .where(
                db.and_(
                    groups_roles.c.group_id.in_([g.id for g in self._groups]),
                    roles_user.c.role_id.is_(None),
                )
            )
            .distinct()
        )
