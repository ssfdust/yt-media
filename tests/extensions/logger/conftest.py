#!/usr/bin/env python
# -*- coding: utf-8 -*-

from typing import Iterator

import pytest
from flask import Flask
from flask.testing import FlaskClient
from kombu import Queue


@pytest.fixture(scope="package")
def queue() -> Queue:
    from smorest_sfs.plugins.rpc import default_queues

    return default_queues.get_default_queue()


@pytest.fixture(scope="package")
def app(queue: Queue) -> Iterator[Flask]:
    # pylint: disable=W0621
    from smorest_sfs.extensions.logger import Logger
    from smorest_sfs.plugins.rpc import Publisher

    flask_app = Flask("TestLogger")
    flask_app.config["AMQP_URL"] = "amqp://"
    Logger(Publisher, flask_app, publish_args={"queue": queue})

    flask_app.add_url_rule("/", "index", lambda: "")

    with flask_app.app_context():
        yield flask_app


@pytest.fixture(scope="package")
def test_client(app: Flask) -> FlaskClient:
    # pylint: disable=W0621
    return app.test_client()
