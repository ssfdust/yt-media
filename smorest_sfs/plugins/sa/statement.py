"""
    SQL语句Builder

    sa raw sql模块
"""

from typing import Dict, List, Any

from loguru import logger
from sqlalchemy.sql.selectable import Select

from .abstract import RenderableStatement
from smorest_sfs.extensions import db


class SAStatement(RenderableStatement):
    sa_sql: Select

    def __init__(self, *args: Any, **kwargs: Any):
        pass

    def get_sa_sql(self) -> Select:
        return self.sa_sql

    def get_keys(self) -> Dict:
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
