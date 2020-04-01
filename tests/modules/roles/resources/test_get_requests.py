#!/usr/bin/env python
# -*- coding: utf-8 -*-
from smorest_sfs.modules.auth import ROLES
from tests._utils.injection import GeneralGet


class TestListView(GeneralGet):

    fixture_names = ("flask_app_client", "flask_app", "regular_user")
    item_view = "Role.RoleItemView"
    listview = "Role.RoleListView"
    view = "Role.RoleView"
    login_roles = [ROLES.RoleManager]

    def test_get_options(self):
        resp = self._get_option()
        assert (
            resp.status_code == 200
            and isinstance(resp.json["data"], list)
            and resp.json["data"][0].keys() == {"id", "name"}
        )

    def test_get_list(self):
        resp = self._get_list(name="e")
        assert (
            resp.status_code == 200
            and isinstance(resp.json["data"], list)
            and resp.json["data"][0].keys()
            >= {"id", "name", "permissions", "user_default", "group_default"}
            and resp.json["data"][0]["permissions"][0].keys() == {"id", "name"}
        )

    def test_get_item(self):
        resp = self._get_item(role_id=1)
        assert (
            resp.status_code == 200
            and isinstance(resp.json["data"], dict)
            and resp.json["data"].keys() > {"id", "name", "created", "modified", "deleted"}
            and resp.json["data"]["permissions"][0].keys() >= {"id", "name"}
        )
