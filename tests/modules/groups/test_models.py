#!/usr/bin/env python
# -*- coding: utf-8 -*-
# pylint: disable=W0611
import pytest

from smorest_sfs.extensions import db
from smorest_sfs.modules.groups.models import Group, groups_roles
from smorest_sfs.modules.roles.models import Role
from smorest_sfs.modules.users.models import groups_users, roles_users
from smorest_sfs.plugins.sa import execute, render_limit_results
from smorest_sfs.services.groups.sqls import DeleteRoleFromGroup, DeleteMultiUserFromGroup
from smorest_sfs.services.groups import parse_group_users_change


@pytest.mark.usefixtures("flask_app")
def test_group() -> None:
    name = str(Group.create(name="test"))
    assert name == "test"
