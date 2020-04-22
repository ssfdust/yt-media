#!/usr/bin/env python
# -*- coding: utf-8 -*-
from typing import Any, Callable, Iterator, Tuple, Type

import pytest
from marshmallow import Schema

from smorest_sfs.modules.logs.models import Log


@pytest.fixture
@pytest.mark.usefixtures("flask_app")
def log_items(
    temp_db_instance_helper: Callable[..., Iterator[Any]],
) -> Iterator[Tuple[Log, Log, Log]]:
    for _ in temp_db_instance_helper(*(Log(name=str(_) + "tqwq") for _ in range(3))):
        yield _


@pytest.fixture
def LogSchema() -> Type[Schema]:
    # pylint: disable=W0621
    from smorest_sfs.modules.logs.schemas import LogSchema

    return LogSchema
