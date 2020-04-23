#!/usr/bin/env python
# -*- coding: utf-8 -*-
from typing import Dict, List

import pytest

from smorest_sfs.modules.auth import ROLES
from smorest_sfs.modules.logs.models import Log
from tests._utils.injection import GeneralGet


class TestLogListView(GeneralGet):

    fixture_names = ("flask_app_client", "flask_app", "regular_user", "log_items")
    view = "Log.LogView"
    login_roles = [ROLES.LogManager]
    log_items: List[Log]

    @pytest.mark.parametrize("params, count", [({"level": "in"}, 0)])
    def test_search_count(self, params: Dict[str, str], count: int) -> None:
        data = self._get_list(**params)
        assert len(data) == count

    def test_get_list(self) -> None:
        data = self._get_list()
        assert data[0].keys() > {"id", "level", "line", "module", "message"}


class TestRespLogListView(GeneralGet):

    fixture_names = ("flask_app_client", "flask_app", "regular_user", "resp_log_items")
    view = "Log.ResponseLogView"
    login_roles = [ROLES.LogManager]
    log_items: List[Log]

    def test_get_list(self) -> None:
        data = self._get_list()
        assert data[0].keys() > {"id", "module", "status_code", "ip", "method", "url"}
