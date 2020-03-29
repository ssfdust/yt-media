#!/usr/bin/env python
# -*- coding: utf-8 -*-

import queue

import pytest

from smorest_sfs.extensions.storage.captcha import CaptchaStore

from tests._utils.uniqueue import UniqueQueue

SENDED = UniqueQueue()

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


def fake_send(self):
    SENDED.put(self.content['url'])


@pytest.fixture
def patched_mail(monkeypatch):
    from smorest_sfs.services.mail import PasswdMailSender

    monkeypatch.setattr(PasswdMailSender, "send", fake_send)
