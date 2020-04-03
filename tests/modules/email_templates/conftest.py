#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pytest

from smorest_sfs.modules.email_templates.models import EmailTemplate
from typing import Callable
from typing import Iterator
from typing import Tuple
from typing import Union


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
