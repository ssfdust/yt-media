#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""测试自定义ma的创建"""


class TestMaCreataion:
    def test_ma_meta(self, app):
        from smorest_sfs.extensions.marshal import ma
        from marshmallow import EXCLUDE

        ma.init_app(app)

        TestSchema = type("TestSchema", (ma.Schema,), dict())

        assert TestSchema.Meta.unknown == EXCLUDE
