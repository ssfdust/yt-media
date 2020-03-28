#!/usr/bin/env python
# -*- coding: utf-8 -*-
import io

import pytest

from smorest_sfs.modules.auth.permissions import ROLES
from tests._utils.injection import FixturesInjectBase


from flask import url_for
class TestStoragesView(FixturesInjectBase):

    fixture_names = ("flask_app_client", "flask_app")

    def test_get(self, regular_user, add_storage):
        with self.flask_app_client.login(regular_user, [ROLES.User]) as client:
            resp = client.get(f"/api/v1/storages/{add_storage.id}")
            assert resp.data == b"abc"

    def test_put(self, regular_user, add_storage):
        with self.flask_app_client.login(regular_user, [ROLES.User]) as client:
            store_id = add_storage.id
            client.put(
                f"/api/v1/storages/{store_id}",
                data={"file": (io.BytesIO(b"789"), "new.txt")},
                content_type="multipart/form-data",
            )
            add_storage.store = None
            resp = client.get(f"/api/v1/storages/{add_storage.id}")
            assert resp.data == b"789"

    def test_delete(self, regular_user, add_storage):
        with self.flask_app_client.login(regular_user, [ROLES.User]) as client:
            resp = client.delete(f"/api/v1/storages/{add_storage.id}")
            after_resp = client.get(f"/api/v1/storages/{add_storage.id}")
            assert resp.json["code"] == 0 and after_resp.status_code == 404


class TestUploadView(FixturesInjectBase):
    fixture_names = ("flask_app_client", "flask_app")

    @pytest.mark.usefixtures("clean_dirs")
    def test_post(self, regular_user):
        with self.flask_app_client.login(regular_user, [ROLES.User]) as client:
            with self.flask_app.test_request_context():
                resp = client.post(
                    url_for("Storages.UploadView", storetype="foo"),
                    data={"file": (io.BytesIO(b"456"), "new.txt")},
                    content_type="multipart/form-data",
                )
                store_id = resp.json["data"]["file_id"]
                resp = client.get(url_for("Storages.StoragesView", file_id=store_id))
                assert resp.data == b"456"
