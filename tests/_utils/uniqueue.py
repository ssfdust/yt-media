#!/usr/bin/env python
# -*- coding: utf-8 -*-

from queue import SimpleQueue


class UniqueQueue(SimpleQueue):
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, "_queue"):
            orig = super(UniqueQueue, cls)
            cls._queue = orig.__new__(cls, *args, **kwargs)

        return cls._queue
