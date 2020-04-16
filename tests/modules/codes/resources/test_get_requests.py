#!/usr/bin/env python
# -*- coding: utf-8 -*-
from typing import List

from smorest_sfs.modules.auth import ROLES
from smorest_sfs.modules.codes.models import Code
from tests._utils.injection import GeneralGet


class TestListView(GeneralGet):

    fixture_names = ("flask_app_client", "flask_app", "regular_user", "project_items")
    listview = "Code.CodeListView"
    login_roles = [ROLES.CodeManager]
    project_items: List[Code]

    def test_get_options(self) -> None:
        self._get_options()
