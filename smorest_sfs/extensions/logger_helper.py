#!/usr/bin/env python
# -*- coding: utf-8 -*-
from .logger import Logger


def create_logger() -> Logger:
    from smorest_sfs.plugins.rpc import Publisher
    from kombu import Queue

    queue = Queue("logger-queue", "logger", durable=True, routing_key="logger")
    return Logger(Publisher, publish_args={"queue": queue})
