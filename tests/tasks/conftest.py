#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest
from celery.contrib.testing import worker
from celery.contrib.testing.app import setup_default_app


@pytest.fixture(scope="package")
def flask_celery(flask_app):
    from smorest_sfs.extensions import celery

    return celery


@pytest.fixture(scope="package")
def flask_celery_app(flask_celery):
    test_app = flask_celery.get_celery_app()
    test_app.loader.import_task_module("celery.contrib.testing.tasks")
    with setup_default_app(test_app):
        test_app.set_default()
        test_app.set_current()
        yield test_app


@pytest.fixture(scope="package")
def flask_celery_worker(flask_celery_app):
    with worker.start_worker(
        flask_celery_app, pool="solo", perform_ping_check=False,
    ) as w:
        yield w
        w.terminate(False)
        w.stop(False)
