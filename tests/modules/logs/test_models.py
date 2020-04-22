#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pytest

from smorest_sfs.modules.logs.models import Log


@pytest.mark.usefixtures("flask_app")
def test_log() -> None:
    name = str(Log.create(name="test"))
    assert name == "test"
