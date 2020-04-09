#!/usr/bin/env python
# -*- coding: utf-8 -*-
from typing import Callable, Iterator, Tuple, Union

import pytest

from smorest_sfs.modules.email_templates.models import EmailTemplate


@pytest.fixture
@pytest.mark.usefixtures("flask_app")
def email_template_items(
    temp_db_instance_helper: Callable,
) -> Iterator[
    Union[Iterator, Iterator[Tuple[EmailTemplate, EmailTemplate, EmailTemplate]]]
]:
    for _ in temp_db_instance_helper(
        *(EmailTemplate(name=str(_), template="qq") for _ in range(3))
    ):
        yield _
