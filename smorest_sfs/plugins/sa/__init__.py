"""
    sa模块
"""
from typing import Any, Union

from smorest_sfs.extensions import db

from .query import SAQuery, query_decorator
from .statement import SAStatement, sql_decorator

__all__ = ["SAStatement", "SAQuery", "sql_decorator", "query_decorator"]


def _execute_sql(sa_sql):
    cursor = db.session.execute(sa_sql)
    return cursor.fetchall()


def _execute_sa(sql: SAStatement):
    sa_sql = sql.get_sa_sql()
    return _execute_sql(sa_sql)


def _execute_query(query: SAQuery):
    return query.get_record()


def execute(sql_cls: Union[SAStatement, SAQuery], *args: Any, **kwargs: Any) -> Any:
    sql = sql_cls(*args, **kwargs)
    if isinstance(sql, SAQuery):
        ret = _execute_query(sql)
    else:
        ret = _execute_sa(sql)

    return ret


def debug_sql(sql_cls: Union[SAStatement, SAQuery], *args: Any, **kwargs: Any):
    sql = sql_cls(*args, **kwargs)
    sql.debug_sql()


def render_limit_results(
    sql_cls: Union[SAStatement, SAQuery], *args: Any, **kwargs: Any
):
    sql = sql_cls(*args, **kwargs)
    sql.render_results()
