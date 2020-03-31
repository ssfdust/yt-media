#!/usr/bin/env python
# -*- coding: utf-8 -*-
from typing import Dict, List

from flask import url_for

import pytest
from smorest_sfs.modules.auth import ROLES
from tests._utils.injection import FixturesInjectBase


class TestGeneralModify(FixturesInjectBase):

    fixture_names = ("flask_app_client", "flask_app", "regular_user")
    cachelst: List[Dict] = []
    item: Dict = {}

    @pytest.mark.parametrize(
        "data",
        [
            {"name": "t1", "description": "qqq"},
            {"name": "t2", "description": "www"},
            {"name": "t3", "description": "aaa"},
        ],
    )
    def test_add(self, data, permissions):
        with self.flask_app_client.login(
            self.regular_user, [ROLES.RoleManager]
        ) as client:
            with self.flask_app.test_request_context():
                url = url_for("Role.RoleView")
                data["permissions"] = permissions
                resp = client.post(url, json=data)
                self.cachelst.append(resp.json["data"])
                assert (
                    resp.status_code == 200
                    and isinstance(resp.json["data"], dict)
                    and resp.json["data"].keys() >= {"id", "name", "permissions"}
                    and resp.json["data"]["permissions"][0].keys() >= {"id", "name"}
                )

    def test_delete(self):
        with self.flask_app_client.login(
            self.regular_user, [ROLES.RoleManager]
        ) as client:
            with self.flask_app.test_request_context():
                url = url_for("Role.RoleView")
                ids = [self.cachelst.pop()["id"] for _ in range(2)]
                resp = client.delete(url, json={"lst": ids})
                assert resp.status_code == 200

    def test_item_modify(self, update_permissions):
        with self.flask_app_client.login(
            self.regular_user, [ROLES.RoleManager]
        ) as client:
            with self.flask_app.test_request_context():
                self.item = self.cachelst[-1]
                url = url_for("Role.RoleItemView", role_id=self.item["id"],)
                self.item.update(
                    {
                        "name": "tt",
                        "description": "qaqa",
                        "permissions": update_permissions,
                    }
                )
                resp = client.put(url, json=self.item,)
                assert (
                    resp.status_code == 200
                    and resp.json["data"]["name"] == "tt"
                    and resp.json["data"]["description"] == "qaqa"
                    and resp.json["data"]["permissions"] == update_permissions
                )

    def test_item_delete(self):
        with self.flask_app_client.login(
            self.regular_user, [ROLES.RoleManager]
        ) as client:
            self.item = self.cachelst[-1]
            with self.flask_app.test_request_context():
                url = url_for("Role.RoleItemView", role_id=self.item["id"],)
                resp = client.delete(url)
                after_resp = client.get(url)
                assert resp.status_code == 200 and after_resp.status_code == 404
