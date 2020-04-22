#!/usr/bin/env python
# -*- coding: utf-8 -*-
from typing import List

from smorest_sfs.modules.auth import ROLES
from smorest_sfs.modules.logs.models import Log
from tests._utils.injection import GeneralGet


class TestListView(GeneralGet):

    fixture_names = ("flask_app_client", "flask_app", "regular_user", "log_items")
    item_view = "Log.LogItemView"
    listview = "Log.LogListView"
    view = "Log.LogView"
    login_roles = [ROLES.LogManager]
    log_items: List[Log]

    def test_get_options(self) -> None:
        self._get_options()

    def test_get_list(self) -> None:
        data = self._get_list(name="t")
        assert data[0].keys() > {"id", "name"}

    def test_get_item(self) -> None:
        data = self._get_item(log_id=self.log_items[0].id)
        assert data.keys() >= {"id", "name"}
