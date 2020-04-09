#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import shutil
import uuid
from typing import Callable, Iterator, Tuple, Type, Union

import pytest
from _pytest.monkeypatch import MonkeyPatch
from flask import Flask
from loguru import logger

from migrations.initial_development_data import (init_email_templates,
                                                 init_permission)
from smorest_sfs.app import ENABLED_MODULES, create_app
from smorest_sfs.extensions.sqla.db_instance import SQLAlchemy  # type: ignore
from smorest_sfs.modules.users.models import Model, User
from smorest_sfs.utils.paths import UploadPath

from ._utils import client, injection, tables, users


class fakeuuid:
    hex = "123456789"


@pytest.fixture
def patch_uuid(monkeypatch: MonkeyPatch):  # type: ignore
    monkeypatch.setattr(uuid, "uuid4", fakeuuid)


@pytest.fixture
def clean_dirs() -> Iterator:
    yield
    for key in ["foo", "new", "bar"]:
        path = UploadPath.get_uploads_subdir(key, withdate=False)
        if path.exists():
            shutil.rmtree(path)


@pytest.fixture(scope="session")
def flask_app() -> Iterator[Flask]:
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
def db(flask_app: Flask) -> Iterator[SQLAlchemy]:
    # pylint: disable=W0613, W0621
    from smorest_sfs.extensions import db as db_instance

    yield db_instance


@pytest.fixture(scope="session")
def flask_app_client(flask_app: Flask) -> client.FlaskClient:
    # pylint: disable=W0613, W0621
    flask_app.test_client_class = client.AutoAuthFlaskClient
    flask_app.response_class = client.JSONResponse
    return flask_app.test_client()


@pytest.fixture(scope="session")
def temp_db_instance_helper(db: SQLAlchemy) -> Callable:  # type: ignore
    # pylint: disable=W0613, W0621
    def temp_db_instance_manager(
        *instances: Model,
    ) -> Iterator[Union[Model, Tuple[Model]]]:
        for instance in instances:
            instance.save()

        if len(instances) == 1:
            yield instances[0]
        else:
            yield instances

        tables.clear_instances(db, instances)

    return temp_db_instance_manager


@pytest.fixture(scope="session")
def regular_user(
    temp_db_instance_helper: Callable[..., Iterator[Model]]
) -> Iterator[User]:
    # pylint: disable=W0613, W0621
    for _ in temp_db_instance_helper(
        users.generate_user_instance(username="regular_user")
    ):
        yield _


@pytest.fixture(scope="session")
def inactive_user(
    temp_db_instance_helper: Callable[..., Iterator[Model]]
) -> Iterator[User]:
    # pylint: disable=W0613, W0621
    for _ in temp_db_instance_helper(
        users.generate_user_instance(username="inactive_user", phonenum="inactive_user")
    ):
        yield _


@pytest.fixture(scope="session")
def forget_passwd_user(
    temp_db_instance_helper: Callable[..., Iterator[Model]]
) -> Iterator[User]:
    # pylint: disable=W0613, W0621
    for _ in temp_db_instance_helper(
        users.generate_user_instance(
            username="forget_passwd_user", phonenum="forget_passwd_user"
        )
    ):
        yield _


@pytest.fixture(scope="session")
def guest_user(
    temp_db_instance_helper: Callable[..., Iterator[Model]]
) -> Iterator[User]:
    # pylint: disable=W0613, W0621
    for _ in temp_db_instance_helper(
        users.generate_user_instance(username="guest_user", phonenum="guest_user")
    ):
        yield _


@pytest.fixture
def inject_logger() -> Iterator:
    injection.inject_logger(logger)
    yield
    injection.uninject_logger(logger)
