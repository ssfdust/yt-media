#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import url_for

from smorest_sfs.modules.auth import ROLES
from tests._utils.injection import FixturesInjectBase


class TestListView(FixturesInjectBase):

    fixture_names = ("flask_app_client", "flask_app", "regular_user")

    def test_get_options(self):
        with self.flask_app_client.login(
            self.regular_user, [ROLES.SuperUser]
        ) as client:
            with self.flask_app.test_request_context():
                url = url_for("Project.ProjectListView")
                resp = client.get(url)
                assert (
                    resp.status_code == 200
                    and isinstance(resp.json["data"], list)
                    and resp.json["data"][0].keys() == {"id", "name"}
                )

    def test_get_list(self):
        with self.flask_app_client.login(
            self.regular_user, [ROLES.SuperUser]
        ) as client:
            with self.flask_app.test_request_context():
                url = url_for("Project.ProjectView", name="t")
                resp = client.get(url)
                assert (
                    resp.status_code == 200
                    and isinstance(resp.json["data"], list)
                    and resp.json["data"][0].keys() > {"id", "name"}
                )


class TestItemView(FixturesInjectBase):

    fixture_names = ("flask_app_client", "flask_app", "regular_user")

    def test_get_item(self):
        with self.flask_app_client.login(
            self.regular_user, [ROLES.SuperUser]
        ) as client:
            with self.flask_app.test_request_context():
                url = url_for(
                    "Project.ProjectItemView", project_id=1
                )
                resp = client.get(url)
                assert (
                    resp.status_code == 200
                    and isinstance(resp.json["data"], dict)
                    and resp.json["data"].keys() > {"id", "name"}
                )
