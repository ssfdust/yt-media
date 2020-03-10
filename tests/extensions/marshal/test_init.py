#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""测试自定义ma的创建"""
from flask import Flask
from smorest_sfs.extensions.marshal import ma
from marshmallow import EXCLUDE


class TestMaCreataion:
    def test_ma_meta(self, app: Flask):

        ma.init_app(app)

        TestSchema = type("TestSchema", (ma.Schema,), dict())

        assert TestSchema.Meta.unknown == EXCLUDE
