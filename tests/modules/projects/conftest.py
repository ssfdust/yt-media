#!/usr/bin/env python
# -*- coding: utf-8 -*-
from typing import Callable, Iterator, Tuple, Union

import pytest

from smorest_sfs.modules.projects.models import Project


@pytest.fixture
@pytest.mark.usefixtures("flask_app")
def project_items(
    temp_db_instance_helper: Callable,
) -> Iterator[Union[Iterator, Iterator[Tuple[Project, Project, Project]]]]:
    for _ in temp_db_instance_helper(
        *(Project(name=str(_) + "tqwq") for _ in range(3))
    ):
        yield _
