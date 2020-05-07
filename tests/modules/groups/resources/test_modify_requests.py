#!/usr/bin/env python
# -*- coding: utf-8 -*-
from typing import Dict

import pytest

from smorest_sfs.modules.auth import ROLES
from smorest_sfs.modules.groups.models import Group
from smorest_sfs.modules.groups.schemas import GroupSchema
from tests._utils.helpers import param_helper
from tests._utils.injection import GeneralModify


class TestGroupModify(GeneralModify):
    items = "group_items"
    fixture_names = ("flask_app_client", "flask_app", "regular_user", "db",) + (items,)
    view = "Group.GroupView"
    item_view = "Group.GroupItemView"
    login_roles = [ROLES.GroupManager]
    model = Group
    delete_param_key = "group_id"
    schema = "GroupSchema"

    def test_add(self) -> None:
        json = {
            "name": "test_add_group",
            "description": "",
            "default": False,
            "roles": [],
            "users": [],
        }
        data = self._add_request(json)
        assert data.keys() > {"id", "name"}

    def test_item_modify(self) -> None:
        data = self._item_modify_request(
            json={
                "name": "qq",
                "description": "",
                "default": True,
                "roles": [],
                "users": [],
            }
        )
        assert data["name"] == "qq"

    def test_item_delete(self) -> None:
        self._item_delete_request()
