"""
    SQL语句Builder

    query模块
"""

from abc import abstractmethod
from functools import wraps
from typing import Dict, List, Type

from loguru import logger

from .helpers import QueryAnalysis
from .statement import SAStatement


class SAQuery(SAStatement):
    @abstractmethod
    def get_record(self):
        raise NotImplementedError

    def render_results(self, size: int = 50):
        query = self.get_render_sql(size)
        analysis = QueryAnalysis(query)
        self.parse_records = lambda x: [analysis.getter(r) for r in x]
        records = query.all()
        self._render_data_table(records)
        table_data = self._render_data_table(records)
        logger.debug("\n" + table_data)


def query_decorator(cls: Type[SAQuery]):
    @wraps(cls)
    def wraper(*args, **kwargs):
        def get_sa_sql(self):
            return self.query.statement

        def get_keys(self) -> List:
            analysis = QueryAnalysis(self.query)
            return analysis.keys

        def get_render_sql(self, size: int = 50):
            return self.query.limit(size)

        @staticmethod
        def parse_records(records: List) -> List[Dict]:
            pass

        cls.get_sa_sql = get_sa_sql

        cls.get_keys = get_keys

        cls.get_render_sql = get_render_sql

        cls.parse_records = parse_records

        return cls(*args, **kwargs)

    return wraper
