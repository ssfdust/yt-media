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
        "data", [{"name": "t1"}, {"name": "t2"}, {"name": "t3"},],
    )
    def test_add(self, data):
        resp = self._add_request(data)
        assert (
            resp.status_code == 200
            and isinstance(resp.json["data"], dict)
            and resp.json["data"].keys() > {"id", "name"}
        )

    def test_delete(self):
        resp, items = self._delete_request()
        assert resp.status_code == 200 and all([i.deleted for i in items])

    def test_item_modify(self):
        resp = self._item_modify_request(json={"name": "tt"})
        assert resp.status_code == 200 and resp.json["data"]["name"] == "tt"

    def test_item_delete(self):
        resp, item = self._item_delete_request()
        assert resp.status_code == 200 and item.deleted
