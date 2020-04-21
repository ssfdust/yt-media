#!/usr/bin/env python
# -*- coding: utf-8 -*-
from typing import Iterator, Type

import pytest
from flask_sqlalchemy import SQLAlchemy
from marshmallow import Schema

from smorest_sfs.services.menus.import_menus import import_menus_from_filepath, models


@pytest.fixture
@pytest.mark.usefixtures("flask_app", "MenuSchema")
def fake_menus(db: SQLAlchemy) -> Iterator[None]:
    import_menus_from_filepath("tests/data/menus/test-menus.xlsx")
    yield
    db.session.execute(
        "TRUNCATE TABLE {} RESTART IDENTITY".format(models.Menu.__tablename__)
    )
    db.session.commit()


@pytest.fixture
def MenuSchema() -> Type[Schema]:
    # pylint: disable=W0621
    from smorest_sfs.modules.menus.schemas import MenuSchema

    return MenuSchema
