#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
测试辅助工具集
"""
from typing import List
import pytest
from smorest_sfs.extensions.sqla.db_instance import SQLAlchemy


class FixturesInjectBase:

    fixture_names = ()

    @pytest.fixture(autouse=True)
    def auto_injector_fixture(self, request):
        names = self.fixture_names
        for name in names:
            setattr(self, name, request.getfixturevalue(name))


def drop_tables(db: SQLAlchemy, table_names: List[str]):
    bind = db.get_engine()
    tables = [db.metadata.tables[table] for table in table_names]
    db.metadata.drop_all(bind=bind, tables=tables)
