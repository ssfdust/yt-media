#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest
from smorest_sfs.extensions.storage.captcha import CaptchaStore


@pytest.fixture
def patch_code(monkeypatch):
    """为编码补丁"""

    def fake_code(self, length: int = 4):
        self._code = "2345"

    monkeypatch.setattr(CaptchaStore, "_decode_code", fake_code)


@pytest.fixture
def permissions():
    from smorest_sfs.modules.auth.permissions import PERMISSIONS

    return [PERMISSIONS.UserEdit, PERMISSIONS.GroupQuery, PERMISSIONS.GroupAdd]