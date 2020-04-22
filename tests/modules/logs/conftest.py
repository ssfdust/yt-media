#!/usr/bin/env python
# -*- coding: utf-8 -*-
from typing import Any, Callable, Iterator, Tuple, Type

import pytest
from marshmallow import Schema

from smorest_sfs.modules.logs.models import Log, ResponseLog


@pytest.fixture
@pytest.mark.usefixtures("flask_app")
def log_items(
    temp_db_instance_helper: Callable[..., Iterator[Any]],
) -> Iterator[Tuple[Log, ...]]:
    for _ in temp_db_instance_helper(
        Log(module="test.info", line=15, level="info", message="test"),
        Log(module="test.info", line=15, level="info", message="test"),
        Log(module="test.info", line=15, level="info", message="test"),
        Log(module="test.debug", line=15, level="debug", message="test"),
        Log(module="test.debug", line=15, level="debug", message="test"),
        Log(module="test.error", line=15, level="error", message="test"),
        Log(module="test.warn", line=15, level="warn", message="test"),
        Log(module="test.warn", line=15, level="warn", message="test"),
    ):
        yield _


@pytest.fixture
@pytest.mark.usefixtures("flask_app")
def resp_log_items(
    temp_db_instance_helper: Callable[..., Iterator[Any]],
) -> Iterator[Tuple[ResponseLog, ...]]:
    for _ in temp_db_instance_helper(
        ResponseLog(
            module="test.test_1",
            status_code=200,
            ip="127.0.0.1",
            method="PUT",
            url="/test/test_1",
        ),
        ResponseLog(
            module="test.test_2",
            status_code=200,
            ip="127.0.0.1",
            method="PUT",
            url="/test/test_2",
        ),
        ResponseLog(
            module="test.test_3",
            status_code=200,
            ip="127.0.0.1",
            method="GET",
            url="/test/test_3",
        ),
        ResponseLog(
            module="test.test_4",
            status_code=200,
            ip="127.0.0.1",
            method="OPTIONS",
            url="/test/test_4",
        ),
        ResponseLog(
            module="test.test_5",
            status_code=200,
            ip="127.0.0.1",
            method="POST",
            url="/test/test_5",
        ),
        ResponseLog(
            module="test.test_6",
            status_code=200,
            ip="127.0.0.1",
            method="POST",
            url="/test/test_6",
        ),
        ResponseLog(
            module="test.test_7",
            status_code=200,
            ip="127.0.0.1",
            method="DELETE",
            url="/test/test_7",
        ),
    ):
        yield _


@pytest.fixture
def LogSchema() -> Type[Schema]:
    # pylint: disable=W0621
    from smorest_sfs.modules.logs.schemas import LogSchema

    return LogSchema
