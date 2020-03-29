#!/usr/bin/env python
# -*- coding: utf-8 -*-
from typing import Dict, List

import pytest
from flask import url_for

from smorest_sfs.modules.auth import ROLES
from tests._utils.injection import FixturesInjectBase


class TestGeneralModify(FixturesInjectBase):

    fixture_names = ("flask_app_client", "flask_app", "regular_user")
    cachelst: List[Dict] = []
    item: Dict = {}

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
            self.regular_user, [ROLES.SuperUser]
        ) as client:
            with self.flask_app.test_request_context():
                url = url_for("EmailTemplate.EmailTemplateView")
                resp = client.post(url, json=data)
                self.cachelst.append(resp.json["data"])
                assert (
                    resp.status_code == 200
                    and isinstance(resp.json["data"], dict)
                    and resp.json["data"].keys() > {"id", "name"}
                )

    def test_delete(self):
        with self.flask_app_client.login(
            self.regular_user, [ROLES.SuperUser]
        ) as client:
            with self.flask_app.test_request_context():
                url = url_for("EmailTemplate.EmailTemplateView")
                ids = [self.cachelst.pop()["id"] for _ in range(2)]
                resp = client.delete(url, json={"lst": ids})
                assert resp.status_code == 200

    def test_item_modify(self):
        with self.flask_app_client.login(
            self.regular_user, [ROLES.SuperUser]
        ) as client:
            with self.flask_app.test_request_context():
                self.item = self.cachelst[-1]
                url = url_for(
                    "EmailTemplate.EmailTemplateItemView",
                    email_template_id=self.item["id"],
                )
                resp = client.put(url, json={"name": "tt", "template": "qaqa"})
                assert (
                    resp.status_code == 200
                    and resp.json["data"]["name"] == "tt"
                    and resp.json["data"]["template"] == "qaqa"
                )

    def test_item_delete(self):
        with self.flask_app_client.login(
            self.regular_user, [ROLES.SuperUser]
        ) as client:
            self.item = self.cachelst[-1]
            with self.flask_app.test_request_context():
                url = url_for(
                    "EmailTemplate.EmailTemplateItemView",
                    email_template_id=self.item["id"],
                )
                resp = client.delete(url)
                after_resp = client.get(url)
                assert resp.status_code == 200 and after_resp.status_code == 404
