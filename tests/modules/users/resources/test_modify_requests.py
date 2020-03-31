#!/usr/bin/env python
# -*- coding: utf-8 -*-
from typing import Dict, List

from flask import url_for

import pytest
from smorest_sfs.modules.auth import ROLES
from tests._utils.injection import FixturesInjectBase


class TestGeneralModify(FixturesInjectBase):

    fixture_names = (
        "flask_app_client",
        "flask_app",
        "regular_user",
        "forget_passwd_user",
        "inactive_user",
        "guest_user",
    )
    cachelst: List[Dict] = []
    item: Dict = {}

    def test_delete(self):
        with self.flask_app_client.login(
            self.regular_user, [ROLES.UserManager]
        ) as client:
            with self.flask_app.test_request_context():
                url = url_for("User.UserView")
                ids = [self.forget_passwd_user.id, self.inactive_user.id]
                resp = client.delete(url, json={"lst": ids})
                assert (
                    resp.status_code == 200
                    and self.forget_passwd_user.deleted
                    and self.inactive_user.deleted
                )

    def test_item_modify(self):
        with self.flask_app_client.login(
            self.regular_user, [ROLES.UserManager]
        ) as client:
            with self.flask_app.test_request_context():
                url = url_for("User.UserItemView", user_id=self.guest_user.id)
                resp = client.put(
                    url,
                    json={
                        "phonenum": "12121212",
                        "username": "guest_user",
                        "confirmed_at": None,
                        "email": "66666",
                        "password": "7777",
                        "active": False,
                        "userinfo": {
                            "first_name": "tt",
                            "last_name": "qaqa",
                            "sex": 2,
                            "age": 13,
                        }
                    },
                )
                assert (
                    resp.status_code == 200
                    and self.guest_user.phonenum == "12121212"
                    and self.guest_user.email == "66666"
                    and self.guest_user.password == "7777"
                    and self.guest_user.nickname == "tt qaqa"
                    and self.guest_user.userinfo.sex_label == "女"
                    and self.guest_user.userinfo.age == 13
                )

    def test_item_delete(self):
        with self.flask_app_client.login(
            self.regular_user, [ROLES.SuperUser]
        ) as client:
            with self.flask_app.test_request_context():
                url = url_for("User.UserItemView", user_id=self.guest_user.id)
                resp = client.delete(url)
                after_resp = client.get(url)
                assert resp.status_code == 200 and after_resp.status_code == 404
