#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pytest
from typing import List

from smorest_sfs.extensions import db
from smorest_sfs.modules.users.models import User, Group, roles_users, groups_users
from smorest_sfs.modules.groups.models import groups_roles
from smorest_sfs.plugins.sa import SAStatement

@pytest.mark.usefixtures("flask_app")
def test_group() -> None:
    name = str(Group.create(name="test"))
    assert name == "test"

@pytest.mark.usefixtures("flask_app")
def test_sqls() -> None:
    db.session.execute(roles_users.insert(values=[[1, 1], [1, 3], [1, 2], [2, 2], [3, 3], [3, 1]]))
    db.session.execute(groups_roles.insert(values=[[1, 1], [1, 2], [2, 1], [2, 2], [2, 3], [3, 2], [3, 3], [3, 5]]))
    class Sql(SAStatement):
        def __init__(self, user: User, groups: List[Group]):
            self._user = user
            self._groups = groups
            self._build_sql()

        def _build_sql(self):
            roles_user = db.alias(db.select([roles_users]).where(roles_users.c.user_id == self._user.id), 'roles_user')
            joined = db.outerjoin(groups_roles, roles_user, groups_roles.c.role_id == roles_user.c.role_id)
            self.sa_sql =  db.select([db.func.coalesce(roles_user.c.user_id, self._user.id).label("user_id"), groups_roles.c.role_id]).select_from(joined).where(
                db.and_(groups_roles.c.group_id.in_([g.id for g in self._groups]), roles_user.c.role_id.is_(None))
            ).distinct()

    sql = Sql(User(id=1), [Group(id=1), Group(id=3)])
    sql.render_results()
