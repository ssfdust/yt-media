"""
    smorest_sfs.plugins.sa.helpers
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    一些辅助函数模块
"""
from flask_sqlalchemy import BaseQuery

from typing import Any, Dict


class QueryAnalysis:
    """分析Query的keys以及parse函数"""

    def __init__(self, query: BaseQuery):
        self.query = query
        self.col_desc = query.column_descriptions
        self.is_direct = self.__is_direct(self.col_desc)
        self.getter = lambda x: x
        self.keys = []
        self._parse()

    @staticmethod
    def __is_direct(col_desc: Dict[str, Any]) -> bool:
        if len(col_desc) > 1:
            return False
        if col_desc[0]["type"] is col_desc[0]["entity"]:
            return True
        return False

    def _parse(self) -> None:
        if self.is_direct:
            entity = self.__extract_entity()
            self.keys = self.__get_entity_col_keys(entity)
            self.getter = lambda x: [getattr(x, key) for key in self.keys]
        else:
            self.keys = [desc["name"] for desc in self.col_desc]

    def __extract_entity(self):
        return self.col_desc[0]["entity"]

    @staticmethod
    def __get_entity_col_keys(entity):
        mapper = getattr(entity, "__mapper__")
        return [attr.key for attr in mapper.column_attrs]
