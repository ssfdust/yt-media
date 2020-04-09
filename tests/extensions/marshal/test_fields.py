#!/usr/bin/env python
# -*- coding: utf-8 -*-
from datetime import datetime

import pytest
from flask import Flask
from marshmallow import Schema, ValidationError


def test_fields_dump(app: Flask, pendulum_field_schema: Schema) -> None:
    with app.app_context():
        data = {"time": datetime(1994, 9, 11, 8, 20)}
        res = pendulum_field_schema.dump(data)
        assert res["time"] == "1994-09-11 16:20:00"


def test_fields_load(app: Flask, pendulum_field_schema: Schema) -> None:
    with app.app_context():
        data = {"time": "1994-09-11 08:20:00"}
        res = pendulum_field_schema.load(data)
        assert str(res["time"]) == "1994-09-11T00:20:00+00:00"


def test_fileds_none_load_handle(app: Flask, pendulum_field_schema: Schema) -> None:
    with app.app_context():
        data = {"time": None}
        res = pendulum_field_schema.load(data)
        assert res["time"] is None


def test_fields_empty_load_handle(app: Flask, pendulum_field_schema: Schema) -> None:
    with app.app_context():
        data = {"time": ""}
        with pytest.raises(ValidationError):
            pendulum_field_schema.load(data)


def test_fileds_none_dump_handle(app: Flask, pendulum_field_schema: Schema) -> None:
    with app.app_context():
        data = {"time": None}
        res = pendulum_field_schema.dump(data)
        assert res["time"] is None
