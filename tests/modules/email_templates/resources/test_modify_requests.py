#!/usr/bin/env python
# -*- coding: utf-8 -*-
from typing import Dict, List

import pytest
from flask import url_for

from smorest_sfs.modules.auth import ROLES
from smorest_sfs.modules.email_templates.models import EmailTemplate
from tests._utils.injection import GeneralModify


class TestEmailTemplateModify(GeneralModify):

    items = "email_template_items"
    fixture_names = (
        "flask_app_client",
        "flask_app",
        "regular_user",
        "email_template_items",
        "db",
    )
    login_roles = [ROLES.EmailTemplateManager]
    item_view = "EmailTemplate.EmailTemplateItemView"
    view = "EmailTemplate.EmailTemplateView"
    delete_param_key = "email_template_id"
    model = EmailTemplate

    @pytest.mark.parametrize(
        "data",
        [
            {"name": "email_template_1", "template": "test_1"},
            {"name": "email_template_2", "template": "test_2"},
            {"name": "email_template_3", "template": "test_3"},
        ],
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
        json = {"name": "tt", "template": "qaqa"}
        resp = self._item_modify_request(json)
        assert (
            resp.status_code == 200
            and resp.json["data"]["name"] == "tt"
            and resp.json["data"]["template"] == "qaqa"
        )

    def test_item_delete(self):
        resp, item = self._item_delete_request()
        assert resp.status_code == 200 and item.deleted
