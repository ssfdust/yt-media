"""
    SQL语句Builder

    query模块
"""

from abc import abstractmethod
from functools import wraps
from typing import Dict, List, Type

from flask_sqlalchemy import BaseQuery
from loguru import logger

from .helpers import QueryAnalysis
from .statement import SAStatement, Select


class SAQuery(SAStatement):
    """用于Query的辅助模块"""

    @abstractmethod
    def get_record(self):
        raise NotImplementedError

    def get_sa_sql(self) -> Select:
        return self.query.statement

    def get_keys(self) -> List[str]:
        analysis = QueryAnalysis(self.query)
        return analysis.keys

    def get_render_sql(self, size: int = 50) -> BaseQuery:
        return self.query.limit(size)

    @staticmethod
    def parse_records(_: List) -> List[Dict]:
        pass

    def render_results(self, size: int = 50):
        query = self.get_render_sql(size)
        analysis = QueryAnalysis(query)
        self.parse_records = lambda x: [analysis.getter(r) for r in x]
        records = query.all()
        table_data = self._render_data_table(records)
        logger.debug("\n" + table_data)
