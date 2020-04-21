#!/usr/bin/env python
# -*- coding: utf-8 -*-

from typing import Any, Callable, Dict, Iterator, List, Tuple, Type

import pytest
from marshmallow import Schema

from smorest_sfs.modules.auth import PERMISSIONS
from smorest_sfs.modules.roles.models import Permission, Role


@pytest.fixture
@pytest.mark.usefixtures("flask_app")
def test_role(temp_db_instance_helper: Callable[..., Iterator[Any]]) -> Iterator[Any]:
    for _ in temp_db_instance_helper(Role(name="test_role")):
        yield _


@pytest.fixture
@pytest.mark.usefixtures("flask_app")
def test_permission(
    temp_db_instance_helper: Callable[..., Iterator[Any]]
) -> Iterator[Any]:
    for _ in temp_db_instance_helper(Permission(name="test_permission")):
        yield _


@pytest.fixture
def test_role_with_permission(test_role: Role, test_permission: Permission) -> Role:
    new_role: Role = test_role.update(permissions=[test_permission])
    return new_role


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
    temp_db_instance_helper: Callable[..., Any],
) -> Iterator[Iterator[Tuple[Role, Role, Role]]]:
    for _ in temp_db_instance_helper(Role(name="1"), Role(name="2"), Role(name="3")):
        yield _


@pytest.fixture
@pytest.mark.usefixtures("flask_app")
def RoleSchema() -> Type[Schema]:
    # pylint: disable=W0621
    from smorest_sfs.modules.roles.schemas import RoleSchema

    return RoleSchema
