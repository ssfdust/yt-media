#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pytest
from flask_sqlalchemy import SQLAlchemy

from smorest_sfs.modules.codes.models import Code
from smorest_sfs.modules.codes.schemas import CodeListSchema, CodeOptsSchema


@pytest.mark.usefixtures("flask_app", "fake_codes")
def test_simple_code() -> None:
    codes = Code.query.filter_by(type_code="test-001").all()
    assert {"A001", "B001", "C001"} == {code.name for code in codes}
