#!/usr/bin/env python
# -*- coding: utf-8 -*-


import pytest

from smorest_sfs.modules import auth, load_module
from tests._utils.uniqueue import UniqueQueue

QUEUE = UniqueQueue()


@pytest.mark.usefixtures("inject_logger")
def test_invaild_module_loads(monkeypatch):
    monkeypatch.setattr(auth, "preload_modules", ["ttt"])
    load_module("auth")
    assert QUEUE.get() == "无法加载{module_name}下的{submodule}".format(
        module_name="auth", submodule="ttt"
    )
