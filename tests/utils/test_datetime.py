#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime

import pendulum
import pytest
from freezegun import freeze_time

from smorest_sfs.utils.datetime import convert_timezone, utcnow, utctoday

FREEZETIME = "1994-09-11 08:20:00"


@freeze_time(FREEZETIME)
def test_utcnow() -> None:
    now = utcnow()

    assert str(now) == FREEZETIME


@freeze_time(FREEZETIME)
def test_utctoday() -> None:
    today = utctoday()

    assert str(today) == "1994-09-11"


@freeze_time(FREEZETIME)
def test_convert_timezone_for_pendulum() -> None:
    pendulum_dt = pendulum.now("utc")
    sh_dt = convert_timezone(pendulum_dt, "Asia/Shanghai")
    assert sh_dt.to_datetime_string() == "1994-09-11 16:20:00"
