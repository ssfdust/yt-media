"""
    SQL语句Builder

    sa raw sql模块
"""

from typing import Any, Dict, List

from loguru import logger
from sqlalchemy.sql.selectable import Select

from smorest_sfs.extensions import db

from .abstract import RenderableStatement


class SAStatement(RenderableStatement):
    sa_sql: Select

    def __init__(self, *args: Any, **kwargs: Any):
        pass

    def get_sa_sql(self) -> Select:
        return self.sa_sql

    def get_keys(self) -> Any:
        return {}

    def get_render_sql(self, size: int) -> Select:
        return self.sa_sql.limit(size)

    @staticmethod
    def parse_records(records: List[Any]) -> List[Dict[str, Any]]:
        return [dict(record.items()) for record in records]

    def render_results(self, size: int = 50) -> None:
        """渲染结果"""
        cursor = db.session.execute(self.get_render_sql(size))
        records = cursor.fetchall()
        table_data = self._render_data_table(records)
        logger.debug("\n" + table_data)
