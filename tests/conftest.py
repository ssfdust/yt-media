#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import shutil
import uuid
from typing import Callable

import pytest
from _pytest.monkeypatch import MonkeyPatch
from flask import Flask

from migrations.initial_development_data import init_permission, init_email_templates
from smorest_sfs.app import create_app, ENABLED_MODULES
from smorest_sfs.extensions.sqla.db_instance import SQLAlchemy
from smorest_sfs.modules.users.models import User
from smorest_sfs.utils.paths import UploadPath

from ._utils import client, users


class fakeuuid:
    hex = "123456789"


@pytest.fixture
def patch_uuid(monkeypatch: MonkeyPatch):
    monkeypatch.setattr(uuid, "uuid4", fakeuuid)


@pytest.fixture
def clean_dirs():
    yield
    for key in ["foo", "new", "bar"]:
        path = UploadPath.get_uploads_subdir(key, withdate=False)
        if path.exists():
            shutil.rmtree(path)


@pytest.fixture(scope="session")
def flask_app() -> Flask:
    # pylint: disable=W0613, W0621
    from smorest_sfs.extensions import db

    os.environ["FLASK_ENV"] = "testing"
    app = create_app(ENABLED_MODULES)

    with app.app_context():
        db.create_all()
        init_permission()
        init_email_templates()
        yield app
        db.session.rollback()
        db.drop_all()


@pytest.yield_fixture(scope="session")
def db(flask_app: Flask) -> SQLAlchemy:
    # pylint: disable=W0613, W0621
    from smorest_sfs.extensions import db as db_instance

    yield db_instance


@pytest.fixture(scope="session")
def flask_app_client(flask_app: Flask):
    # pylint: disable=W0613, W0621
    flask_app.test_client_class = client.AutoAuthFlaskClient
    flask_app.response_class = client.JSONResponse
    return flask_app.test_client()


@pytest.fixture(scope="session")
def temp_db_instance_helper(db) -> Callable:
    # pylint: disable=W0613, W0621
    def temp_db_instance_manager(instance: db.Model) -> db.Model:
        instance.save()

        yield instance

        mapper = instance.__class__.__mapper__
        if instance not in db.session:
            db.session.add(instance)

        d = instance.__class__.query.filter(
            mapper.primary_key[0] == mapper.primary_key_from_instance(instance)[0]
        ).delete()
        db.session.commit()

    return temp_db_instance_manager


@pytest.fixture(scope="session")
def regular_user(temp_db_instance_helper: Callable) -> User:
    # pylint: disable=W0613, W0621
    for _ in temp_db_instance_helper(
        users.generate_user_instance(username="regular_user")
    ):
        yield _


@pytest.fixture(scope="session")
def inactive_user(temp_db_instance_helper: Callable) -> User:
    # pylint: disable=W0613, W0621
    for _ in temp_db_instance_helper(
        users.generate_user_instance(username="inactive_user", phonenum="inactive_user")
    ):
        yield _


@pytest.fixture(scope="session")
def forget_passwd_user(temp_db_instance_helper: Callable) -> User:
    # pylint: disable=W0613, W0621
    for _ in temp_db_instance_helper(
        users.generate_user_instance(
            username="forget_passwd_user", phonenum="forget_passwd_user"
        )
    ):
        yield _


@pytest.fixture(scope="session")
def guest_user(temp_db_instance_helper: Callable) -> User:
    # pylint: disable=W0613, W0621
    for _ in temp_db_instance_helper(
        users.generate_user_instance(username="guest_user", phonenum="guest_user")
    ):
        yield _
