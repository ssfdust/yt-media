#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""测试基本类型"""
import pytest
from smorest_sfs.extensions.marshal.bases import BaseMsgSchema
from smorest_sfs.extensions.marshal.bases import BaseIntListSchema
from smorest_sfs.extensions.marshal.bases import BasePageSchema


class TestBasesMaClass:
    def test_base_msg(self):

        schema = BaseMsgSchema()
        data = schema.dump({})
        assert data["msg"] == "success" and data["code"] == 0

    @pytest.mark.parametrize(
        "data, result",
        [
            ({"data": []}, []),
            ({"lst": []}, []),
            ({"lst": [1, 2, 3, 4]}, [1, 2, 3, 4]),
        ],
    )
    def test_base_int_list(self, data, result):

        schema = BaseIntListSchema()
        rv = schema.load(data)
        assert rv["lst"] == result

    @pytest.mark.parametrize(
        "data, result",
        [
            (
                {
                    "meta": {
                        "page": 1,
                        "per_page": 10,
                        "total": 100,
                        "links": {
                            "next": "nurl",
                            "prev": "purl",
                            "first": "furl",
                            "last": "lurl",
                        },
                    }
                },
                {
                    "code": 0,
                    "meta": {
                        "page": 1,
                        "per_page": 10,
                        "total": 100,
                        "links": {
                            "next": "nurl",
                            "prev": "purl",
                            "first": "furl",
                            "last": "lurl",
                        },
                    },
                    "msg": "success",
                },
            )
        ],
    )
    def test_base_page(self, data, result):

        schema = BasePageSchema()
        rv = schema.dump(data)
        assert rv == result
