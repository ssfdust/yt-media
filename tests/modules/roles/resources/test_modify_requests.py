#!/usr/bin/env python
# -*- coding: utf-8 -*-
from typing import Dict

import pytest

from smorest_sfs.modules.roles.models import ROLES, Role
from smorest_sfs.modules.roles.schemas import RoleSchema
from tests._utils.injection import GeneralModify


class TestRoleModify(GeneralModify):
    items = "role_items"
    view = "Role.RoleView"
    item_view = "Role.RoleItemView"
    login_roles = [ROLES.RoleManager]
    model = Role
    schema = RoleSchema
    delete_param_key = "role_id"

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
            {"name": "t1", "description": "t1"},
            {"name": "t2", "description": "t2"},
            {"name": "t3", "description": "t3"},
        ],
    )
    def test_add(self, data, permissions):
        data["permissions"] = permissions
        resp = self._add_request(data)
        assert (
            resp.status_code == 200
            and isinstance(resp.json["data"], dict)
            and resp.json["data"].keys() >= {"id", "name", "permissions"}
            and resp.json["data"]["permissions"][0].keys() == {"id", "name"}
        )

    def test_delete(self):
        resp, items = self._delete_request()
        assert resp.status_code == 200 and all([i.deleted for i in items])

    def test_item_modify(self, update_permissions):
        json = self._get_dumped_modified_item()
        json.update(
            {
                "name": "tt",
                "description": "qaqa",
                "permissions": update_permissions,
            }
        )
        resp = self._item_modify_request(json)
        assert (
            resp.status_code == 200
            and resp.json["data"]["name"] == "tt"
            and resp.json["data"]["description"] == "qaqa"
            and resp.json["data"]["permissions"] == update_permissions
        )

    def test_item_delete(self):
        resp, item = self._item_delete_request() 
        assert resp.status_code == 200 and item.deleted
