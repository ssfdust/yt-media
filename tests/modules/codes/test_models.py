#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pytest
from flask_sqlalchemy import SQLAlchemy
from smorest_sfs.modules.codes.models import Code
from smorest_sfs.modules.codes.schemas import CodeOptsSchema, CodeListSchema


@pytest.mark.usefixtures("flask_app", "fake_codes")
def test_simple_code() -> None:
    codes = Code.query.filter_by(type_code="test-001").all()
    assert {"A001", "B001", "C001"} == {code.name for code in codes}


@pytest.mark.usefixtures("flask_app", "fake_codes")
def test_complex_code(db: SQLAlchemy) -> None:
    schema = CodeOptsSchema()
    nested_schema = CodeListSchema()
    codes = Code.get_tree(
        db.session,
        json=True,
        json_fields=schema.dump,
        query=lambda q: q.filter_by(type_code="test-002"),
    )
    data = nested_schema.dump({"data": codes})
    assert data["data"] == [
        {"id": 4, "name": "A001"},
        {"id": 5, "name": "B001", "children": [{"id": 7, "name": "B010"}]},
        {
            "id": 6,
            "name": "C001",
            "children": [
                {"id": 8, "name": "C010"},
                {"id": 9, "name": "C011"},
                {"id": 10, "name": "C100"},
            ],
        },
    ]
