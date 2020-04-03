#!/usr/bin/env python
# -*- coding: utf-8 -*-

from typing import Callable


import pytest
from smorest_sfs.modules.auth import PERMISSIONS
from smorest_sfs.modules.roles.models import Permission, Role
from typing import Any
from typing import Dict
from typing import List
from typing import Iterator
from typing import Tuple
from typing import Union


@pytest.fixture
@pytest.mark.usefixtures("flask_app")
def test_role(temp_db_instance_helper: Callable):
    for _ in temp_db_instance_helper(Role(name="test_role")):
        yield _


@pytest.fixture
@pytest.mark.usefixtures("flask_app")
def test_permission(temp_db_instance_helper: Callable):
    for _ in temp_db_instance_helper(Permission(name="test_permission")):
        yield _


@pytest.fixture
def test_role_with_permission(test_role: Role, test_permission: Permission) -> Role:
    return test_role.update(permissions=[test_permission])


@pytest.fixture
@pytest.mark.usefixtures("flask_app")
def permissions() -> List[Dict[str, Any]]:
    return [
        {"id": p.id, "name": p.name}
        for p in Permission.get_by_names(PERMISSIONS.RoleAdd, PERMISSIONS.RoleQuery)
    ]


@pytest.fixture
@pytest.mark.usefixtures("flask_app")
def update_permissions() -> List[Dict[str, Any]]:
    return [
        {"id": p.id, "name": p.name}
        for p in Permission.get_by_names(
            PERMISSIONS.RoleAdd, PERMISSIONS.RoleQuery, PERMISSIONS.RoleDelete
        )
    ]


@pytest.fixture
@pytest.mark.usefixtures("flask_app")
def role_items(
    temp_db_instance_helper: Callable,
) -> Iterator[Union[Iterator, Iterator[Tuple[Role, Role, Role]]]]:
    for _ in temp_db_instance_helper(Role(name="1"), Role(name="2"), Role(name="3")):
        yield _
