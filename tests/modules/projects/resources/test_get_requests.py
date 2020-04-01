#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import url_for

from smorest_sfs.modules.auth import ROLES
from tests._utils.injection import GeneralGet


class TestListView(GeneralGet):

    fixture_names = ("flask_app_client", "flask_app", "regular_user", "project_items")
    item_view = "Project.ProjectItemView"
    listview = "Project.ProjectListView"
    view = "Project.ProjectView"
    login_roles = [ROLES.ProjectManager]

    def test_get_options(self):
        resp = self._get_option()
        assert (
            resp.status_code == 200
            and isinstance(resp.json["data"], list)
            and resp.json["data"][0].keys() == {"id", "name"}
        )

    def test_get_list(self):
        resp = self._get_list(name="t")
        assert (
            resp.status_code == 200
            and isinstance(resp.json["data"], list)
            and resp.json["data"][0].keys() > {"id", "name"}
        )

    def test_get_item(self):
        resp = self._get_item(project_id=self.project_items[0].id)
        assert (
            resp.status_code == 200
            and isinstance(resp.json["data"], dict)
            and resp.json["data"].keys() >= {"id", "name"}
        )
