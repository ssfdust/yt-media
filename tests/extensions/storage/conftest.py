#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
from typing import Iterator

import pytest
from flask import Flask


@pytest.fixture(scope="package", autouse=True)
def captcha_app() -> Iterator[Flask]:
    app = Flask("TestStorage")
    app.config["CELERY_BROKER_URL"] = os.environ.get("AMQP_URI") or "amqp://"
    with app.app_context():
        yield app
