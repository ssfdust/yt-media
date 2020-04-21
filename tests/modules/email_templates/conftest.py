#!/usr/bin/env python
# -*- coding: utf-8 -*-
from typing import Any, Callable, Iterator, Tuple, Type

import pytest
from marshmallow import Schema

from smorest_sfs.modules.email_templates.models import EmailTemplate


@pytest.fixture
@pytest.mark.usefixtures("flask_app")
def email_template_items(
    temp_db_instance_helper: Callable[..., Iterator[Any]],
) -> Iterator[Tuple[EmailTemplate, EmailTemplate, EmailTemplate]]:
    for _ in temp_db_instance_helper(
        *(EmailTemplate(name=str(_), template="qq") for _ in range(3))
    ):
        yield _


@pytest.fixture
def EmailTemplateSchema() -> Type[Schema]:
    # pylint: disable=W0621
    from smorest_sfs.modules.email_templates.schemas import EmailTemplateSchema

    return EmailTemplateSchema
