#!/usr/bin/env python
# -*- coding: utf-8 -*-

class QueryAnalysis:
    def __init__(self, query):
        self.query = query
        self.col_desc = query.column_descriptions
        self.is_direct = self.__is_direct(self.col_desc)
        self.getter = lambda x: x
        self.keys = []
        self._parse()

    @staticmethod
    def __is_direct(col_desc):
        if len(col_desc) > 1:
            return False
        if col_desc[0]["type"] is col_desc[0]["entity"]:
            return True
        return False

    def _parse(self):
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
