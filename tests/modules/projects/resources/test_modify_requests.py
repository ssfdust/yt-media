#!/usr/bin/env python
# -*- coding: utf-8 -*-
from typing import Dict, List

import pytest
from smorest_sfs.modules.auth import ROLES
from smorest_sfs.modules.projects.models import Project
from tests._utils.injection import GeneralModify


class TestProjectModify(GeneralModify):
    items = "project_items"
    fixture_names = ("flask_app_client", "flask_app", "regular_user", "db",) + (items,)
    view = "Project.ProjectView"
    item_view = "Project.ProjectItemView"
    login_roles = [ROLES.ProjectManager]
    model = Project
    delete_param_key = "project_id"

    @pytest.mark.parametrize(
        "data", [{"name": "project_1"}, {"name": "project_2"}, {"name": "project_3"},],
    )
    def test_add(self, data):
        data = self._add_request(data)
        assert data.keys() > {"id", "name"}

    def test_delete(self):
        self._delete_request()

    def test_item_modify(self):
        data = self._item_modify_request(json={"name": "tt"})
        assert data["name"] == "tt"

    def test_item_delete(self):
        self._item_delete_request()
