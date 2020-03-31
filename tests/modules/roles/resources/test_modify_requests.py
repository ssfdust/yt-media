#!/usr/bin/env python
# -*- coding: utf-8 -*-
from typing import Dict, List

import pytest
from flask import url_for

from smorest_sfs.modules.roles.models import ROLES, Role
from smorest_sfs.modules.roles.schemas import RoleSchema as schema
from tests._utils.injection import FixturesInjectBase


class TestGeneralModify(FixturesInjectBase):

    fixture_names = (
        "flask_app_client",
        "flask_app",
        "regular_user",
        "db",
        "role_items",
    )

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
                assert (
                    resp.status_code == 200
                    and isinstance(resp.json["data"], dict)
                    and resp.json["data"].keys() >= {"id", "name", "permissions"}
                    and resp.json["data"]["permissions"][0].keys() >= {"id", "name"}
                )
                Role.query.filter_by(id=resp.json["data"]["id"]).delete()
                self.db.session.commit()

    def test_delete(self):
        with self.flask_app_client.login(
            self.regular_user, [ROLES.RoleManager]
        ) as client:
            with self.flask_app.test_request_context():
                url = url_for("Role.RoleView")
                ids = [r.id for r in self.role_items]
                resp = client.delete(url, json={"lst": ids})
                assert resp.status_code == 200

    def test_item_modify(self, update_permissions):
        with self.flask_app_client.login(
            self.regular_user, [ROLES.RoleManager]
        ) as client:
            with self.flask_app.test_request_context():
                item = self.role_items[-1]
                url = url_for("Role.RoleItemView", role_id=item.id)
                json = schema().dump(item)
                json.update(
                    {
                        "name": "tt",
                        "description": "qaqa",
                        "permissions": update_permissions,
                    }
                )
                resp = client.put(url, json=json)
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
            with self.flask_app.test_request_context():
                url = url_for("Role.RoleItemView", role_id=1)
                resp = client.delete(url)
                after_resp = client.get(url)
                assert resp.status_code == 200 and after_resp.status_code == 404
