#!/usr/bin/env python
# -*- coding: utf-8 -*-
from typing import Any, Callable, Iterator, Tuple, Type

import pytest
from marshmallow import Schema
from smorest_sfs.modules.groups.models import Group


@pytest.fixture
@pytest.mark.usefixtures("flask_app")
def group_items(
    temp_db_instance_helper: Callable[..., Iterator[Any]],
) -> Iterator[Tuple[Group, Group, Group]]:
    for _ in temp_db_instance_helper(
        *(Group(name=str(_) + "tqwq") for _ in range(3))
    ):
        yield _


@pytest.fixture
def GroupSchema() -> Type[Schema]:
    # pylint: disable=W0621
    from smorest_sfs.modules.groups.schemas import GroupSchema
    return GroupSchema