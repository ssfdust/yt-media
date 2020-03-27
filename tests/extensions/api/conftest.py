#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from typing import Any, Type
from flask import Flask
import pytest
import marshmallow as ma
from smorest_sfs.extensions.sqla.db_instance import SQLAlchemy
from smorest_sfs.extensions import babel
from smorest_sfs.extensions.api import Api
from smorest_sfs.extensions.sqla import SurrogatePK, Model
from smorest_sfs.extensions.marshal.bases import BasePageSchema
from tests._utils.tables import drop_tables


TABLES = ["test_pagination"]


def init_flaskapp(db: SQLAlchemy) -> Flask:
    # pylint: disable=W0621
    flask_app = Flask("TestApi")
    flask_app.config["OPENAPI_VERSION"] = "3.0.2"
    flask_app.config["BABEL_DEFAULT_TIMEZONE"] = "Asia/Shanghai"
    flask_app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
        "PG_URI", "postgresql://postgres@localhost/postgres"
    )

    babel.init_app(flask_app)
    db.init_app(flask_app)

    return flask_app


@pytest.fixture(scope="package")
def db() -> SQLAlchemy:
    from smorest_sfs.extensions import db as db_instance

    return db_instance


@pytest.fixture(scope="package")
def TestPagination(db: SQLAlchemy) -> Model:
    # pylint: disable=W0621
    class TestPagination(SurrogatePK, Model):

        __tablename__ = "test_pagination"

        name = db.Column(db.String(10))

    return TestPagination


@pytest.fixture(scope="package")
def app(db: SQLAlchemy) -> Flask:
    # pylint: disable=W0621
    flask_app = init_flaskapp(db)

    with flask_app.app_context():
        db.create_all()
        yield flask_app
        db.session.rollback()
        drop_tables(db, TABLES)


@pytest.fixture(scope="package")
def api(app: Flask) -> Api:
    # pylint: disable=W0621
    return Api(app)


@pytest.fixture(scope="package")
def TestSchema() -> ma.Schema:
    # pylint: disable=W0621
    class TestSchema(ma.Schema):
        id = ma.fields.Int(dump_only=True)
        name = ma.fields.String()

    return TestSchema


@pytest.fixture(scope="package")
def TestPageSchema(TestSchema: ma.Schema) -> ma.Schema:
    # pylint: disable=W0621
    class TestPageSchema(BasePageSchema):

        data = ma.fields.List(ma.fields.Nested(TestSchema))

    return TestPageSchema


@pytest.fixture(scope="package", autouse=True)
def setup_db(app: Flask, db: SQLAlchemy, TestPagination: Type[Model]):
    # pylint: disable=W0613, W0621
    db.create_all()
    data = [TestPagination(name=str(i + 1)) for i in range(20)]
    db.session.bulk_save_objects(data)
    db.session.commit()
