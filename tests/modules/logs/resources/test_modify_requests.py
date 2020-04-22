#!/usr/bin/env python
# -*- coding: utf-8 -*-
from typing import Dict

import pytest

from smorest_sfs.modules.auth import ROLES
from smorest_sfs.modules.logs.models import Log
from smorest_sfs.modules.logs.schemas import LogSchema
from tests._utils.helpers import param_helper
from tests._utils.injection import GeneralModify


class TestLogModify(GeneralModify):
    items = "log_items"
    fixture_names = ("flask_app_client", "flask_app", "regular_user", "db",) + (items,)
    view = "Log.LogView"
    item_view = "Log.LogItemView"
    login_roles = [ROLES.LogManager]
    model = Log
    delete_param_key = "log_id"
    schema = "LogSchema"

    @pytest.mark.parametrize("data", param_helper(name="log"))
    def test_add(self, data: Dict[str, str]) -> None:
        data = self._add_request(data)
        assert data.keys() > {"id", "name"}

    def test_delete(self) -> None:
        self._delete_request()

    def test_item_modify(self) -> None:
        data = self._item_modify_request(json={"name": "tt"})
        assert data["name"] == "tt"

    def test_item_delete(self) -> None:
        self._item_delete_request()
