#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import pytest
from marshmallow import Schema, fields
from flask import Flask
from smorest_sfs.extensions.sqla import CRUDMixin, SurrogatePK
from smorest_sfs.extensions import babel


def get_inited_app(db):
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
def db():
    from smorest_sfs.extensions.sqla import db as db_instance

    return db_instance


@pytest.fixture(scope="package")
def TestCRUDTable(db):
    # pylint: disable=W0621
    class TestCRUDTable(SurrogatePK, db.Model):
        __tablename__ = "sqla_test_crud_table"

        name = db.Column(db.String(80), unique=True)

    return TestCRUDTable


@pytest.fixture(scope="package")
def TestParentTable(db):
    # pylint: disable=W0621
    class TestParentTable(SurrogatePK, db.Model):
        __tablename__ = "test_crud_parent_table"

    return TestParentTable


@pytest.fixture(scope="package")
def TestChildTable(db, TestParentTable):
    # pylint: disable=W0621
    class TestChildTable(SurrogatePK, db.Model):
        __tablename__ = "test_crud_child_table"
        pid = db.Column(db.Integer, db.ForeignKey(TestParentTable.id))
        parnet = db.relationship(
            TestParentTable,
            backref=db.backref("children", active_history=True),
            active_history=True,
        )
    return TestChildTable


@pytest.fixture(scope="package")
def tables(TestCRUDTable, TestChildTable):
    # pylint: disable=W0613, W0621
    pass


@pytest.fixture(scope="package", autouse=True)
def app(db, tables):
    # pylint: disable=W0621, W0613
    flask_app = get_inited_app(db)

    with flask_app.app_context():
        db.create_all()
        yield flask_app
        db.session.rollback()
        bind = db.get_engine()
        tables = [db.metadata.tables[table]
                  for table in ["sqla_test_crud_table"]]
        db.metadata.drop_all(bind=bind, tables=tables)

@pytest.fixture(scope="package")
def TestChildSchema():
    # pylint: disable=W0621, W0613
    class TestChildSchema(Schema):
        id = fields.Int()
        pid = fields.Int()
        name = fields.Str()
    return TestChildSchema
