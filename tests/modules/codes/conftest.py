#!/usr/bin/env python
# -*- coding: utf-8 -*-
from typing import Any, Callable, Iterator, Tuple

import pytest
from flask_sqlalchemy import SQLAlchemy

from smorest_sfs.services.codes import import_codes_from_dir
from smorest_sfs.modules.codes.models import Code


@pytest.fixture
@pytest.mark.usefixtures("flask_app")
def fake_codes(db: SQLAlchemy) -> Iterator[None]:
    import_codes_from_dir("tests/data/codes/")
    yield
    db.session.execute("truncate table {}".format(Code.__tablename__))
    db.session.commit()
