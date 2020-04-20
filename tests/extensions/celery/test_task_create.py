#!/usr/bin/env python
# -*- coding: utf-8 -*-

from typing import Any

from smorest_sfs.extensions import Celery


def test_celery_creation(
    celery_ext: Celery, celery_sess_app: Any, celery_sess_worker: Any
):
    # pylint: disable=W0613
    @celery_ext.task("mul")
    def mul(x, y):  # type: ignore
        return x * y

    celery_sess_worker.reload()

    assert mul.delay(4, 4).get(timeout=1) == 16
    celery_sess_worker.terminate()
