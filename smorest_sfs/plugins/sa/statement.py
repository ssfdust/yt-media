"""
    SQL语句Builder

    sa raw sql模块
"""

from functools import wraps
from typing import Dict, List
from sqlalchemy.engine.result import RowProxy
from .abstract import RenderableStatement


class SAStatement(RenderableStatement):
    def get_sa_sql(self):
        pass

    def get_keys(self):
        pass

    def get_render_sql(self, size):
        pass

    @staticmethod
    def parse_records(records: List[RowProxy]):
        pass


def sql_decorator(cls: SAStatement):
    @wraps(cls)
    def wraper(*args, **kwargs):
        def get_sa_sql(self):
            return self.sa_sql

        def get_keys(self) -> Dict:
            return {}

        def get_render_sql(self, size: int = 50):
            return self.sa_sql.limit(size)

        @staticmethod
        def parse_records(records: List[RowProxy]) -> List[Dict]:
            return [dict(record.items()) for record in records]

        cls.get_sa_sql = get_sa_sql

        cls.get_keys = get_keys

        cls.get_render_sql = get_render_sql

        cls.parse_records = parse_records

        return cls(*args, **kwargs)

    return wraper
