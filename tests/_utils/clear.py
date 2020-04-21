#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Flask
from loguru import logger
from .celery import disconnect


def clear_dummy(app: Flask) -> None:
    logger.remove(app.extensions["logger_ext"].handler_id)
    disconnect(app)
