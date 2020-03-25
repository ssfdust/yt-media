#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""测试auth"""

from queue import Queue

import pytest

from tests.utils.injection import FixturesInjectBase
from smorest_sfs.services.auth.confirm import generate_confirm_token
from smorest_sfs.services.auth.auth import login_user

MAIL_QUEUE = Queue()


class TestAuthModule(FixturesInjectBase):

    fixture_names = ("flask_app_client", "inactive_user", "regular_user")

    @pytest.mark.parametrize(
        "captcha, code, token",
        [("2345", 200, "1212"), ("1111", 403, "1212"), ("1111", 403, "1211"),],
    )
    @pytest.mark.usefixtures("flask_app", "regular_user", "patch_code")
    def test_user_login_captcha(self, captcha: str, code: int, token: str):
        self.flask_app_client.get("/api/v1/auth/captcha?token=1212")
        login_data = {
            "email": "regular_user@email.com",
            "password": "regular_user_password",
            "token": token,
            "captcha": captcha,
        }
        resp = self.flask_app_client.post("/api/v1/auth/login", json=login_data)
        assert resp.status_code == code

    @pytest.mark.parametrize(
        "username, password, active, code",
        [
            ("test", "test", True, 404),
            ("inactive_user@email.com", "test", True, 403),
            ("inactive_user@email.com", "inactive_user_password", True, 200),
            ("inactive_user@email.com", "inactive_user_password", False, 403),
        ],
    )
    @pytest.mark.usefixtures("flask_app", "patch_code")
    def test_user_login_status(
        self, username: str, password: str, active: bool, code: int
    ):
        self.inactive_user.update(active=active)
        self.flask_app_client.get("/api/v1/auth/captcha?token=1234")
        login_data = {
            "email": username,
            "password": password,
            "token": "1234",
            "captcha": "2345",
        }
        resp = self.flask_app_client.post("/api/v1/auth/login", json=login_data)
        assert resp.status_code == code

    def test_user_confirm(self):
        self.regular_user.update(confirmed_at=None)
        token = generate_confirm_token(self.regular_user, "confirm")
        resp = self.flask_app_client.get("/api/v1/auth/confirm?token={}".format(token))
        after_resp = self.flask_app_client.get(
            "/api/v1/auth/confirm?token={}".format(token)
        )
        assert (
            resp.status_code == 200
            and self.regular_user.active
            and self.regular_user.confirmed_at
            and after_resp.status_code == 401
        )

    def test_login_jwt_cannot_use_at_confirm(self):
        token = login_user(self.regular_user)['tokens']['access_token']
        resp = self.flask_app_client.get("/api/v1/auth/confirm?token={}".format(token))
        assert resp.status_code == 403

    #  @pytest.mark.parametrize(
    #      "email, code", [("test", 404), ("forget_passwd_user@email.com", 200), ]
    #  )
    #  def test_user_forget_password(
    #      self, flask_app_client, patched_mail, email, code, forget_passwd_user
    #  ):
    #      resp = flask_app_client.post(
    #          "/api/v1/auth/forget-password", json={"email": email}
    #      )
    #      forget_passwd_user.update(active=True)
    #      assert resp.status_code == code
    #      if resp.status_code == 200:
    #          url = MAIL_QUEUE.get(timeout=3)
    #          resp = flask_app_client.get(url)
    #          assert resp.status_code == 200
    #          resp = flask_app_client.put(
    #              url, json={"password": "1234567", "confirm_password": "123456"}
    #          )
    #          assert resp.status_code == 501
    #          resp = flask_app_client.put(
    #              url, json={"password": "123456", "confirm_password": "123456"}
    #          )
    #          assert resp.status_code == 200
    #          assert forget_passwd_user.verify_and_update_password("123456")
    #          resp = flask_app_client.get(url)
    #          assert resp.status_code == 401
    #
    #  def test_user_refresh_token(
    #      self, flask_app_client, regular_user, patch_code, flask_app
    #  ):
    #      flask_app_client.get("/api/v1/auth/captcha?token=refresh_token")
    #      login_data = {
    #          "email": regular_user.email,
    #          "password": "regular_user_password",
    #          "token": "refresh_token",
    #          "captcha": "2345",
    #      }
    #      resp = flask_app_client.post("/api/v1/auth/login", json=login_data)
    #      refresh_token = resp.json["data"]["tokens"]["refresh_token"]
    #      headers = {"Authorization": "Bearer {}".format(refresh_token)}
    #      resp = flask_app_client.post("/api/v1/auth/refresh", headers=headers)
    #      assert resp.status_code == 200
    #      access_token = resp.json["data"]["access_token"]
    #      headers = {"Authorization": "Bearer {}".format(access_token)}
    #      resp = flask_app_client.post(
    #          "/api/v1/auth/logout",
    #          headers=headers,
    #          json={"refresh_token": refresh_token},
    #      )
    #      assert resp.status_code == 200
    #      resp = flask_app_client.post(
    #          "/api/v1/auth/logout",
    #          headers=headers,
    #          json={"refresh_token": refresh_token},
    #      )
    #      assert resp.status_code == 401
