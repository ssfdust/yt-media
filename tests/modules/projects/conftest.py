#!/usr/bin/env python
# -*- coding: utf-8 -*-
from typing import Any, Callable, Iterator, Tuple, Type

import pytest
from marshmallow import Schema
from smorest_sfs.modules.projects.models import Project


@pytest.fixture
@pytest.mark.usefixtures("flask_app")
def project_items(
    temp_db_instance_helper: Callable[..., Iterator[Any]],
) -> Iterator[Tuple[Project, Project, Project]]:
    for _ in temp_db_instance_helper(
        *(Project(name=str(_) + "tqwq") for _ in range(3))
    ):
        yield _


@pytest.fixture
def ProjectSchema() -> Type[Schema]:
    # pylint: disable=W0621
    from smorest_sfs.modules.projects.schemas import ProjectSchema
    return ProjectSchema