#!/usr/bin/env python
# -*- coding: utf-8 -*-
from typing import Dict, List

import pytest
from flask import url_for

from smorest_sfs.modules.auth import ROLES
from smorest_sfs.modules.projects.models import Project
from tests._utils.injection import FixturesInjectBase


class TestGeneralModify(FixturesInjectBase):

    fixture_names = (
        "flask_app_client",
        "flask_app",
        "regular_user",
        "project_items",
        "db",
    )

    @pytest.mark.parametrize(
        "data",
        [
            {"name": "t1", "template": "qqq"},
            {"name": "t2", "template": "www"},
            {"name": "t3", "template": "aaa"},
        ],
    )
    def test_add(self, data):
        with self.flask_app_client.login(
            self.regular_user, [ROLES.ProjectManager]
        ) as client:
            with self.flask_app.test_request_context():
                url = url_for("Project.ProjectView")
                resp = client.post(url, json=data)
                assert (
                    resp.status_code == 200
                    and isinstance(resp.json["data"], dict)
                    and resp.json["data"].keys() > {"id", "name"}
                )
                Project.query.filter_by(id=resp.json["data"]["id"]).delete()
                self.db.session.commit()

    def test_delete(self):
        with self.flask_app_client.login(
            self.regular_user, [ROLES.ProjectManager]
        ) as client:
            with self.flask_app.test_request_context():
                url = url_for("Project.ProjectView")
                ids = [i.id for i in self.project_items[:1]]
                resp = client.delete(url, json={"lst": ids})
                assert resp.status_code == 200 and all(
                    [i.deleted for i in self.project_items[:1]]
                )

    def test_item_modify(self):
        with self.flask_app_client.login(
            self.regular_user, [ROLES.ProjectManager]
        ) as client:
            with self.flask_app.test_request_context():
                url = url_for(
                    "Project.ProjectItemView",
                    project_id=self.project_items[-1].id,
                )
                resp = client.put(url, json={"name": "tt", "template": "qaqa"})
                assert (
                    resp.status_code == 200
                    and resp.json["data"]["name"] == "tt"
                )

    def test_item_delete(self):
        with self.flask_app_client.login(
            self.regular_user, [ROLES.ProjectManager]
        ) as client:
            with self.flask_app.test_request_context():
                url = url_for(
                    "Project.ProjectItemView",
                    project_id=self.project_items[-1].id,
                )
                resp = client.delete(url)
                after_resp = client.get(url)
                assert resp.status_code == 200 and after_resp.status_code == 404
