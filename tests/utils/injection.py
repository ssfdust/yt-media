#!/usr/bin/env python
# -*- coding: utf-8 -*-

from .uniqueue import UniqueQueue


def log_to_queue(record):
    queue = UniqueQueue()
    queue.put(record.record["message"])
    return record


def inject_logger(logger):
    logger.add(log_to_queue, serialize=False)
