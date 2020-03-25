#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
测试插件中的sa辅助函数
"""
import pytest
import pyperclip
from loguru import logger
from tests.utils.injection import inject_logger
from tests.utils.uniqueue import UniqueQueue
from tests.extensions.sqla.test_sqla import ItemsFixtureBase


class TestSAPlugin(ItemsFixtureBase):
    fixture_names = ("TestCRUDTable", "TestSASql")
    raw_sql = (
        "SELECT sqla_test_crud_table.name "
        "\nFROM sqla_test_crud_table"
        " \nWHERE sqla_test_crud_table.name = '{name}'"
    )
    table_str = "╒════════╕\n" "│ name   │\n" "╞════════╡\n" "│ bbc    │\n" "╘════════╛"

    @pytest.mark.usefixtures("TestTableTeardown", "crud_items")
    @pytest.mark.parametrize("name, count", [("bbc", 1), ("aac", 0)])
    def test_sql_could_run(self, db, name, count):
        sa_sql = self.TestSASql(name).get_sa_sql()
        cursor = db.session.execute(sa_sql)
        assert len(cursor.fetchall()) == count

    @pytest.mark.parametrize("name", ["bbc", "aac"])
    def test_raw_sql_should_rendered(self, name):
        test_sql = self.TestSASql(name)
        assert test_sql.get_raw_sql() == self.raw_sql.format(name=name)

    @pytest.mark.usefixtures("TestTableTeardown", "crud_items")
    def test_table_should_rendered(self):
        inject_logger(logger)
        test_sql = self.TestSASql("bbc")
        test_sql.render_results()
        assert self._get_debug() == "\n" + self.table_str

    @pytest.mark.usefixtures("TestTableTeardown", "crud_items")
    def test_debug_should_rendered(self):
        test_sql = self.TestSASql("bbc")
        test_sql.debug_sql()
        assert self._get_debug() == "\n" + self.raw_sql.format(
            name="bbc"
        ) and pyperclip.paste() == self.raw_sql.format(name="bbc")

    def _get_debug(self):
        queue = UniqueQueue()
        return queue.get(timeout=1)
