#!/usr/bin/env python
# -*- coding: utf-8 -*-
from typing import List

from smorest_sfs.modules.auth import ROLES
from smorest_sfs.modules.logs.models import Log
from tests._utils.injection import GeneralGet


class TestLogListView(GeneralGet):

    fixture_names = ("flask_app_client", "flask_app", "regular_user", "log_items")
    view = "Log.LogView"
    login_roles = [ROLES.LogManager]
    log_items: List[Log]

    def test_get_list(self) -> None:
        data = self._get_list(name="t")
        assert data[0].keys() > {"id", "name"}


class TestRespLogListView(GeneralGet):

    fixture_names = ("flask_app_client", "flask_app", "regular_user", "resp_log_items")
    view = "Log.ResponseLogView"
    login_roles = [ROLES.LogManager]
    log_items: List[Log]

    def test_get_list(self) -> None:
        data = self._get_list(name="t")
        assert data[0].keys() > {"id", "name"}
