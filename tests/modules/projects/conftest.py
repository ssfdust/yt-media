#!/usr/bin/env python
# -*- coding: utf-8 -*-
from typing import Any, Callable, Iterator, Tuple

import pytest

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
