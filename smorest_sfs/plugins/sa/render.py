#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    SQL语句Builder

    渲染表格模块
"""
from typing import List
from abc import ABC, abstractmethod, abstractstaticmethod
from sqlalchemy.engine.result import RowProxy
from tabulate import tabulate


class TableRender(ABC):
    """
    生成渲染表模块

    通过tabulate生成表格
    get_keys获取键名, parse_records获取表格内容
    """

    @abstractmethod
    def get_keys(self):
        raise NotImplementedError

    @abstractstaticmethod
    def parse_records(records: List[RowProxy]):
        raise NotImplementedError

    def _render_data_table(self, records: List[RowProxy]) -> str:
        headers = self.get_keys()
        records = self.parse_records(records)
        return tabulate(records, headers=headers, tablefmt="fancy_grid")
