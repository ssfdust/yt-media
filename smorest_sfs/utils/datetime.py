#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import datetime, date


def utcnow() -> datetime:
    return datetime.utcnow()


def _utctoday(now: datetime) -> date:
    return now.date()


def utctoday() -> date:
    now = utcnow()
    return _utctoday(now)
