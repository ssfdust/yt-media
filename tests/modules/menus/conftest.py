#!/usr/bin/env python
# -*- coding: utf-8 -*-
from typing import Iterator

import pytest
from flask_sqlalchemy import SQLAlchemy

from smorest_sfs.services.menus.import_menus import import_menus_from_filepath, models


@pytest.fixture
@pytest.mark.usefixtures("flask_app")
def fake_menus(db: SQLAlchemy) -> Iterator[None]:
    import_menus_from_filepath("tests/data/menus/test-menus.xlsx")
    yield
    db.session.execute(
        "TRUNCATE TABLE {} RESTART IDENTITY".format(models.Menu.__tablename__)
    )
    db.session.commit()
