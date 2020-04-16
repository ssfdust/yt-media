#!/usr/bin/env python
# -*- coding: utf-8 -*-
from typing import Any, Callable, Iterator, Tuple

import pytest
from flask_sqlalchemy import SQLAlchemy

from smorest_sfs.modules.codes.models import Code
from smorest_sfs.services.codes import import_codes_from_dir


@pytest.fixture
@pytest.mark.usefixtures("flask_app")
def fake_codes(db: SQLAlchemy) -> Iterator[None]:
    import_codes_from_dir("tests/data/codes/")
    yield
    db.session.execute("TRUNCATE TABLE {} RESTART IDENTITY".format(Code.__tablename__))
    db.session.commit()
