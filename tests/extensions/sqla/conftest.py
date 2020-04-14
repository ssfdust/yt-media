#!/usr/bin/env python
# -*- coding: utf-8 -*-
# pylint: disable=missing-docstring

import datetime
import os
from typing import Any, Iterator, Type

import pytest
from flask import Flask
from marshmallow import Schema, fields

from smorest_sfs.extensions import babel
from smorest_sfs.extensions.sqla import Model, SurrogatePK
from smorest_sfs.extensions.sqla.db_instance import SQLAlchemy
from smorest_sfs.plugins.sa import SAQuery, SAStatement
from tests._utils.tables import drop_tables

FAKE_TIME = datetime.datetime(1994, 9, 11, 8, 20)
TABLES = [
    "sqla_test_crud_table",
    "test_crud_child_table",
    "test_crud_parent_table",
]


def get_inited_app(db: SQLAlchemy) -> Flask:
    # pylint: disable=W0621
    flask_app = Flask("TestSqla")
    flask_app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
        "PG_URI", "postgresql://postgres@localhost/postgres"
    )
    flask_app.config["BABEL_DEFAULT_TIMEZONE"] = "Asia/Shanghai"
    db.init_app(flask_app)
    babel.init_app(flask_app)

    return flask_app


@pytest.fixture(scope="package")
def db() -> SQLAlchemy:
    from smorest_sfs.extensions.sqla import db as db_instance

    return db_instance


@pytest.fixture(scope="package")
def TestCRUDTable(db: SQLAlchemy) -> Type[Model]:
    # pylint: disable=W0621
    class TestCRUDTable(SurrogatePK, Model):
        __tablename__ = "sqla_test_crud_table"

        name = db.Column(db.String(80), unique=True)

    return TestCRUDTable


@pytest.fixture(scope="package")
def TestParentTable(db: SQLAlchemy) -> Type[Model]:
    # pylint: disable=W0621
    class TestParentTable(SurrogatePK, Model):
        __tablename__ = "test_crud_parent_table"
        name = db.Column(db.String(80), unique=True)

    return TestParentTable


@pytest.fixture(scope="package")
def TestChildTable(db: SQLAlchemy, TestParentTable: Type[Model]) -> Type[Model]:
    # pylint: disable=W0621
    class TestChildTable(SurrogatePK, Model):
        __tablename__ = "test_crud_child_table"
        name = db.Column(db.String(80), unique=True)
        pid = db.Column(db.Integer, db.ForeignKey(TestParentTable.id))
        parnet = db.relationship(
            TestParentTable,
            backref=db.backref("children", active_history=True),
            active_history=True,
        )

    return TestChildTable


@pytest.fixture(scope="package")
def tables(TestCRUDTable: Type[Model], TestChildTable: Type[Model]) -> None:
    # pylint: disable=W0613, W0621
    pass


@pytest.fixture(scope="package", autouse=True)
def app(db: SQLAlchemy, tables: Any) -> Iterator[Flask]:
    # pylint: disable=W0621, W0613
    flask_app = get_inited_app(db)

    with flask_app.app_context():
        db.create_all()
        yield flask_app
        db.session.rollback()
        drop_tables(db, TABLES)


@pytest.fixture(scope="package")
def TestChildSchema() -> Type[Schema]:
    # pylint: disable=W0621, W0613
    class TestChildSchema(Schema):
        id = fields.Int()
        pid = fields.Int()
        name = fields.Str()
        deleted = fields.Boolean()
        modified = fields.DateTime()
        created = fields.DateTime()

    return TestChildSchema


@pytest.fixture(scope="package")
def TestParentSchema(TestChildSchema: Type[Schema]) -> Type[Schema]:
    # pylint: disable=W0621, W0613
    class TestParentSchema(TestChildSchema):
        children = fields.List(fields.Nested(TestChildSchema))

        class Meta:
            exclude = ["pid"]

    return TestParentSchema


@pytest.fixture
def TestTableTeardown(db: SQLAlchemy) -> Iterator[None]:
    # pylint: disable=W0621, W0613
    yield
    for table in [
        "sqla_test_crud_table",
        "test_crud_child_table",
        "test_crud_parent_table",
    ]:
        db.session.execute(f"TRUNCATE TABLE {table} CASCADE")
    db.session.commit()


@pytest.fixture
def TestSASql(db: SQLAlchemy, TestCRUDTable: Type[Model]) -> Type[SAStatement]:
    # pylint: disable=W0621, W0613
    class TestSASql(SAStatement):
        def __init__(self, name: str) -> None:
            self.sa_sql = db.select([TestCRUDTable.name]).where(
                TestCRUDTable.name == name
            )

    return TestSASql


@pytest.fixture
def TestOneTableQuery(db: SQLAlchemy, TestCRUDTable: Type[Model]) -> Type[SAQuery]:
    # pylint: disable=W0621, W0613
    class TestOneTableQuery(SAQuery):
        def __init__(self) -> None:
            self.query = TestCRUDTable.query.filter(TestCRUDTable.name == "bbc")

        def get_record(self) -> Any:
            return self.query.all()

    return TestOneTableQuery


@pytest.fixture
def TestTwoTablesQuery(
    db: SQLAlchemy, TestCRUDTable: Type[Model], TestChildTable: Type[Model]
) -> Type[SAQuery]:
    # pylint: disable=W0621, W0613
    class TestTwoTablesQuery(SAQuery):
        def __init__(self) -> None:
            self.query = db.session.query(
                TestCRUDTable,
                TestChildTable,
                TestChildTable.name,
                TestCRUDTable.name,
                TestCRUDTable.id.label("crud_id"),
            ).filter(TestCRUDTable.name == "bbc")

        def get_record(self) -> Any:
            return self.query.all()

    return TestTwoTablesQuery


@pytest.fixture
def TestOneColQuery(db: SQLAlchemy, TestCRUDTable: Type[Model]) -> Type[SAQuery]:
    # pylint: disable=W0621, W0613
    class TestOneColQuery(SAQuery):
        def __init__(self) -> None:
            self.query = db.session.query(TestCRUDTable.name).filter(
                TestCRUDTable.name == "bbc"
            )

        def get_record(self) -> Any:
            return self.query.all()

    return TestOneColQuery
