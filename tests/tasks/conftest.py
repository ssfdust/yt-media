#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest
from celery.contrib.testing import worker
from celery.contrib.testing.app import setup_default_app


@pytest.fixture(scope="package")
def flask_celery(flask_app, celery_session_app):
    from smorest_sfs.extensions import celery

    celery.update_celery(celery_session_app)

    return celery


@pytest.fixture(scope="package")
def flask_celery_app(flask_celery):
    return flask_celery.get_celery_app()


@pytest.fixture(scope="package")
def flask_celery_worker(flask_celery_app):
    with worker.start_worker(
        flask_celery_app, pool="solo", perform_ping_check=False,
    ) as w:
        yield w
