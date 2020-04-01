#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pytest
from smorest_sfs.modules.auth import ROLES
from tests._utils.injection import GeneralGet


class TestListView(GeneralGet):

    login_roles = [ROLES.UserManager, ROLES.User]
    listview = "User.UserListView"
    view = "User.UserView"
    item_view = "User.UserItemView"

    fixture_names = ("flask_app_client", "flask_app", "regular_user")

    def test_get_options(self):
        resp = self._get_option()
        assert (
            resp.status_code == 200
            and isinstance(resp.json["data"], list)
            and resp.json["data"][0].keys() == {"id", "nickname"}
        )

    @pytest.mark.parametrize("name", ["qqq", "aaa", "regular"])
    def test_get_list(self, name):
        self.regular_user.userinfo.update(first_name="nqqqn", last_name="baaab")
        resp = self._get_list(name=name)
        assert (
            resp.status_code == 200
            and isinstance(resp.json["data"], list)
            and resp.json["data"][0].keys() > {"id", "nickname"}
            and resp.json["data"][0]["id"] == self.regular_user.id
            and resp.json["data"][0]["userinfo"]["first_name"] == "nqqqn"
            and resp.json["data"][0]["userinfo"]["last_name"] == "baaab"
        )

    def test_get_userinfo(self):
        resp = self._get_view("User.UserSelfView")
        assert (
            resp.status_code == 200
            and resp.json["data"]["username"] == self.regular_user.username
        )

    def test_get_item(self):
        resp = self._get_item(user_id=self.regular_user.id)
        assert (
            resp.status_code == 200
            and isinstance(resp.json["data"], dict)
            and resp.json["data"].keys() >= {"id", "nickname"}
        )
