#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
测试辅助工具集
"""
from typing import List
from smorest_sfs.extensions.sqla.db_instance import SQLAlchemy


def drop_tables(db: SQLAlchemy, table_names: List[str]):
    bind = db.get_engine()
    tables = [db.metadata.tables[table] for table in table_names]
    db.metadata.drop_all(bind=bind, tables=tables)
