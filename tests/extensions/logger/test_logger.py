#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pytest
from flask.testing import FlaskClient
from kombu import Queue
from loguru import logger

from smorest_sfs.plugins.rpc import Subscriber


class TestLog:
    subscriber: Subscriber

    @pytest.fixture(autouse=True)
    def setup_cls(self, queue: Queue) -> None:
        setattr(self, "subscriber", Subscriber(queue))

    def test_log_api(self, test_client: FlaskClient) -> None:
        test_client.get("/")
        for i in self.subscriber.subscribe():
            assert i["status_code"] == 200

    @pytest.mark.usefixtures("app")
    def test_logger_handler(self) -> None:
        logger.debug("test1")
        for i in self.subscriber.subscribe():
            assert i["message"] == "test1"
