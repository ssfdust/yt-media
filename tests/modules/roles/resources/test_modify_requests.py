#!/usr/bin/env python
# -*- coding: utf-8 -*-
from typing import Dict

import pytest
from smorest_sfs.modules.roles.models import ROLES, Role
from smorest_sfs.modules.roles.schemas import RoleSchema
from tests._utils.injection import GeneralModify
from tests._utils.helpers import param_helper


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
        "json",
        param_helper(name="role", description="desc")
    )
    def test_add(self, json, permissions):
        json["permissions"] = permissions
        data = self._add_request(json)
        assert data.keys() >= {"id", "name", "permissions"} and data["permissions"][
            0
        ].keys() == {"id", "name"}

    def test_delete(self):
        self._delete_request()

    def test_item_modify(self, update_permissions):
        json = self._get_dumped_modified_item()
        json.update(
            {"name": "tt", "description": "qaqa", "permissions": update_permissions,}
        )
        data = self._item_modify_request(json)
        assert (
            data["name"] == "tt"
            and data["description"] == "qaqa"
            and data["permissions"] == update_permissions
        )

    def test_item_delete(self):
        self._item_delete_request()
