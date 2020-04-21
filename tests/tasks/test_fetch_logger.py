#!/usr/bin/env python
# -*- coding: utf-8 -*-

def test_fetch_logger(flask_celery, flask_celery_worker):
    breakpoint()
    result = flask_celery.delay("get-logger")
    result.get()
