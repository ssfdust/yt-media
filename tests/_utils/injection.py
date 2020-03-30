#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pytest
from .uniqueue import UniqueQueue


def log_to_queue(record):
    queue = UniqueQueue()
    queue.put(record.record["message"])
    return record


def inject_logger(logger):
    logger.add(log_to_queue, serialize=False)

def uninject_logger(logger):
    logger.remove()



class FixturesInjectBase:

    fixture_names = ()

    @pytest.fixture(autouse=True)
    def auto_injector_fixture(self, request):
        names = self.fixture_names
        for name in names:
            setattr(self, name, request.getfixturevalue(name))
