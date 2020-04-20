#!/usr/bin/env python
# -*- coding: utf-8 -*-

from typing import Any, Iterator, Type

import celery
import pytest
from celery.contrib.testing import worker
from celery.contrib.testing.app import setup_default_app
from flask import Flask

from smorest_sfs.extensions.celery import Celery


@pytest.fixture(scope="package")
def config() -> Type[Any]:
    class TestConfig:
        CELERY_MONGODB_SCHEDULER_COLLECTION = "schedules"
        CELERY_RESULT_BACKEND = "redis://"
        CELERY_BROKER_URL = "amqp://"
        CELERY_ACCEPT_CONTENT = ["json", "json"]

    return TestConfig


@pytest.fixture(scope="package")
def app(config: Any) -> Flask:
    # pylint: disable=W0621
    flask_app = Flask("TestCelery")
    flask_app.config.from_object(config)

    return flask_app


@pytest.fixture(scope="package")
def celery_ext(app: Flask) -> Celery:
    # pylint: disable=W0621
    celery_extension = Celery(app)

    return celery_extension


@pytest.fixture(scope="package")
def celery_sess_app(celery_ext: Celery) -> Iterator[celery.Celery]:
    # pylint: disable=W0621
    test_app = celery_ext.get_celery_app()
    test_app.loader.import_task_module("celery.contrib.testing.tasks")
    with setup_default_app(test_app):
        test_app.set_default()
        test_app.set_current()
        yield test_app


@pytest.fixture(scope="package")
def celery_sess_worker(celery_sess_app: celery.Celery) -> Iterator[Any]:
    # pylint: disable=W0621
    with worker.start_worker(
        celery_sess_app, pool="solo", perform_ping_check=False,
    ) as w:
        yield w
