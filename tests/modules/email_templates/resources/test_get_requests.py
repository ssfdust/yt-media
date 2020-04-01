#!/usr/bin/env python
# -*- coding: utf-8 -*-
from smorest_sfs.modules.auth import ROLES
from tests._utils.injection import GeneralGet


class TestListView(GeneralGet):

    login_roles = [ROLES.EmailTemplateManager]
    fixture_names = ("flask_app_client", "flask_app", "regular_user")
    listview = "EmailTemplate.EmailTemplateListView"
    view = "EmailTemplate.EmailTemplateView"
    item_view = "EmailTemplate.EmailTemplateItemView"

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
            and resp.json["data"][0].keys() > {"id", "name", "template"}
        )

    def test_get_item(self):
        resp = self._get_item(email_template_id=1)
        assert (
            resp.status_code == 200
            and isinstance(resp.json["data"], dict)
            and resp.json["data"].keys() > {"id", "name", "deleted", "template"}
        )
