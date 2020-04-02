#!/usr/bin/env python
# -*- coding: utf-8 -*-
from typing import Dict, List

from flask import url_for

import pytest
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
        data = self._add_request(data)
        assert data.keys() >= {"id", "name", "template"}

    def test_delete(self):
        self._delete_request()

    def test_item_modify(self):
        json = {"name": "tt", "template": "qaqa"}
        data = self._item_modify_request(json)
        assert data["name"] == "tt" and data["template"] == "qaqa"

    def test_item_delete(self):
        self._item_delete_request()
