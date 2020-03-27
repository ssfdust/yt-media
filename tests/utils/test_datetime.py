#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime

from freezegun import freeze_time

from smorest_sfs.utils.datetime import utcnow, utctoday

FREEZETIME = "1994-09-11 08:20:00"


@freeze_time(FREEZETIME)
def test_utcnow():
    now = utcnow()

    assert str(now) == FREEZETIME


@freeze_time(FREEZETIME)
def test_utctoday():
    today = utctoday()

    assert str(today) == "1994-09-11"
