#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
from flask import Flask
import pytest


@pytest.fixture(scope="package", autouse=True)
def captcha_app() -> Flask:
    app = Flask("TestStorage")
    app.config["CELERY_BROKER_URL"] = os.environ.get("AMQP_URI") or "amqp://"
    with app.app_context():
        yield app
