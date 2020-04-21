#!/usr/bin/env python
# -*- coding: utf-8 -*-

from typing import Any

from flask import Flask

import celery
import pytest
from celery.contrib.testing import worker
from smorest_sfs.extensions import Celery


@pytest.fixture(scope="package", autouse=True)
def flask_celery(flask_app: Flask, celery_session_app: celery.Celery) -> Celery:
    # pylint: disable=W0621
    from smorest_sfs.extensions import Celery

    celery = Celery()
    celery.init_app(flask_app)

    celery.update_celery(celery_session_app)

    return celery


@pytest.fixture(scope="package", autouse=True)
def flask_celery_app(flask_celery: Celery) -> celery.Celery:
    # pylint: disable=W0621
    celery_app = flask_celery.get_celery_app()
    celery_app.loader.import_task_module("smorest_sfs.tasks")
    return celery_app


@pytest.fixture(scope="package", autouse=True)
def flask_celery_worker(flask_celery_app: celery.Celery) -> Any:
    # pylint: disable=W0621
    with worker.start_worker(
        flask_celery_app, pool="solo", perform_ping_check=False,
    ) as w:
        yield w
