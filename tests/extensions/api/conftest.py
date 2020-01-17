#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest
from flask import Flask
import marshmallow as ma
from smorest_sfs.extensions import babel
from smorest_sfs.extensions.api import Api
from smorest_sfs.extensions.sqla import SurrogatePK, Model
from smorest_sfs.extensions.marshal.bases import BasePageSchema


all_tables = ["test_pagination"]


def init_flaskapp(db):
    flask_app = Flask("TestApi")
    flask_app.config["OPENAPI_VERSION"] = "3.0.2"
    flask_app.config["BABEL_DEFAULT_TIMEZONE"] = "Asia/Shanghai"
    flask_app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite://"

    babel.init_app(flask_app)
    db.init_app(flask_app)

    return flask_app


@pytest.fixture(scope="package")
def db():
    from smorest_sfs.extensions import db as db_instance
    return db_instance


@pytest.fixture(scope="package")
def TestPagination(db):
    # pylint: disable=W0621
    class TestPagination(SurrogatePK, Model):

        __tablename__ = "test_pagination"

        name = db.Column(db.String(10))
    return TestPagination


@pytest.fixture(scope="package")
def available_tables(db, TestPagination):
    # pylint: disable=W0621
    return [db.metadata.tables[table] for table in all_tables]


@pytest.fixture(scope="package")
def app(db, available_tables):
    # pylint: disable=W0621
    flask_app = init_flaskapp(db)

    with flask_app.app_context():
        db.create_all()
        yield flask_app
        engine = db.get_engine()
        db.metadata.drop_all(bind=engine, tables=available_tables)


@pytest.fixture(scope="package")
def api(app):
    # pylint: disable=W0621
    return Api(app)


@pytest.fixture(scope="package")
def TestSchema():
    # pylint: disable=W0621
    class TestSchema(ma.Schema):
        id = ma.fields.Int(dump_only=True)
        name = ma.fields.String()
    return TestSchema


@pytest.fixture(scope="package")
def TestPageSchema(TestSchema):
    # pylint: disable=W0621
    class TestPageSchema(BasePageSchema):

        data = ma.fields.List(ma.fields.Nested(TestSchema))

    return TestPageSchema


@pytest.fixture(scope="package", autouse=True)
def setup_db(app, db, TestPagination):
    db.create_all()

    data = [TestPagination(name=str(i + 1)) for i in range(20)]
    db.session.bulk_save_objects(data)
    db.session.commit()
