#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    SQL语句Builder

    abc模块
"""

from abc import ABC, abstractmethod, abstractstaticmethod
from typing import List
from sqlalchemy.dialects import postgresql
from sqlalchemy.sql.selectable import Select
from sqlalchemy.engine.result import RowProxy
from loguru import logger
import pyperclip
from smorest_sfs.extensions import db
from .render import TableRender


class StatementAbstract(ABC):
    @abstractmethod
    def get_sa_sql(self) -> Select:
        raise NotImplementedError

    def get_raw_sql(self) -> str:
        sa_sql = self.get_sa_sql()
        compiled_sql = sa_sql.compile(
            dialect=postgresql.dialect(), compile_kwargs={"literal_binds": True},
        )
        return str(compiled_sql)

    def debug_sql(self, need_copy=True):
        raw_sql = self.get_raw_sql()
        logger.debug("\n" + raw_sql)
        if need_copy:
            pyperclip.copy(raw_sql)


class RenderableStatement(StatementAbstract, TableRender):
    @abstractmethod
    def get_sa_sql(self) -> Select:
        raise NotImplementedError

    @abstractmethod
    def get_keys(self) -> List[str]:
        raise NotImplementedError

    @abstractmethod
    def get_render_sql(self, size: int) -> Select:
        raise NotImplementedError

    @abstractstaticmethod
    def parse_records(records: List[RowProxy]):
        raise NotImplementedError

    def render_results(self, size: int = 50):
        cursor = db.session.execute(self.get_render_sql(size))
        records = cursor.fetchall()
        table_data = self._render_data_table(records)
        logger.debug("\n" + table_data)
