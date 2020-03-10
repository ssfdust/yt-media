"""
    SQL语句Builder

    query模块
"""

from functools import wraps
from .render import TableRender
from .abstract import RenderableStatement


class SAQuery(RenderableStatement, TableRender):
    def get_sa_sql(self):
        pass


def query_decorator(cls: SAQuery):
    @wraps(cls)
    def wraper(*args, **kwargs):
        def get_sa_sql(self):
            return self.query.statement

        cls.get_sa_sql = get_sa_sql

        return cls(*args, **kwargs)

    return wraper
