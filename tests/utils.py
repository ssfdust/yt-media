#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pytest


class FixturesInjectBase:

    fixture_names = ()

    @pytest.fixture(autouse=True)
    def auto_injector_fixture(self, request):
        names = self.fixture_names
        for name in names:
            setattr(self, name, request.getfixturevalue(name))


def drop_tables(db, table_names):
    bind = db.get_engine()
    tables = [db.metadata.tables[table] for table in table_names]
    db.metadata.drop_all(bind=bind, tables=tables)
