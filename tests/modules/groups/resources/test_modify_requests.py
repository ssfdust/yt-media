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

    def test_delete(self) -> None:
        self._delete_request()
