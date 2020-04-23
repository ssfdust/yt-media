#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pytest

from smorest_sfs.modules.logs.models import Log, ResponseLog


@pytest.mark.usefixtures("flask_app")
def test_log() -> None:
    item = Log.create(module="test", line=13, level="info", message="test")
    assert str(item) == "test"
    item.hard_delete()


@pytest.mark.usefixtures("flask_app")
def test_resp_log() -> None:
    item = ResponseLog.create(url="test", method="POST", ip="1.0.0.0", status_code=200)
    assert str(item) == "POST test"
    item.hard_delete()


@pytest.mark.usefixtures("flask_app", "log_items")
def test_schema() -> None:
    from smorest_sfs.modules.logs.schemas import LogParamSchema
    from datetime import date

    schema = LogParamSchema()
    data = {"created_date": "2019-09-01", "module": "test_1"}
    assert schema.load(data) == {"created_date": date(2019, 9, 1), "module": "test_1"}
