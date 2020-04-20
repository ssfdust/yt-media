#!/usr/bin/env python
# -*- coding: utf-8 -*-

from typing import Any, Optional
from kombu import Connection, Exchange, Queue
from flask import current_app


class RPCBase:
    def __init__(
        self, queue: Queue, value: Optional[Any] = None, limit: int = 999,
    ):
        self.limit = limit
        self.value = value
        self.queue = queue
        self.exchange = Exchange(self.queue.exchange)
        self.conn = Connection(current_app.config["AMQP_URL"], heartbeat=0)
