#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import url_for

import pytest
from smorest_sfs.modules.auth import ROLES
from tests._utils.injection import FixturesInjectBase


class TestListView(FixturesInjectBase):

    fixture_names = ("flask_app_client", "flask_app", "regular_user")

    def test_get_options(self):
        with self.flask_app_client.login(
            self.regular_user, [ROLES.UserManager]
        ) as client:
            with self.flask_app.test_request_context():
                url = url_for("User.UserListView")
                resp = client.get(url)
                assert (
                    resp.status_code == 200
                    and isinstance(resp.json["data"], list)
                    and resp.json["data"][0].keys() == {"id", "nickname"}
                )

    @pytest.mark.parametrize("name", ["qqq", "aaa", "regular"])
    def test_get_list(self, name):
        with self.flask_app_client.login(
            self.regular_user, [ROLES.UserManager]
        ) as client:
            with self.flask_app.test_request_context():
                self.regular_user.userinfo.update(first_name="nqqqn", last_name="baaab")
                url = url_for("User.UserView", name=name)
                resp = client.get(url)
                assert (
                    resp.status_code == 200
                    and isinstance(resp.json["data"], list)
                    and resp.json["data"][0].keys() > {"id", "nickname"}
                    and resp.json["data"][0]["id"] == self.regular_user.id
                )


class TestItemView(FixturesInjectBase):

    fixture_names = ("flask_app_client", "flask_app", "regular_user")

    def test_get_item(self):
        with self.flask_app_client.login(
            self.regular_user, [ROLES.SuperUser]
        ) as client:
            with self.flask_app.test_request_context():
                url = url_for("User.UserItemView", user_id=self.regular_user.id)
                resp = client.get(url)
                assert (
                    resp.status_code == 200
                    and isinstance(resp.json["data"], dict)
                    and resp.json["data"].keys() >= {"id", "nickname"}
                )
