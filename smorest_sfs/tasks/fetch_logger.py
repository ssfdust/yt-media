#!/usr/bin/env python
# -*- coding: utf-8 -*-


from kombu import Queue
from smorest_sfs.extensions import celery
from smorest_sfs.plugins.rpc import Subscriber


@celery.task("get-logger")
def get_logs_from_subcriber() -> None:
    queue = Queue("logger-queue", "logger", durable=True, routing_key="logger")
    subscriber = Subscriber(queue, limit=5000)
    for i in subscriber.subscribe():
        assert i
