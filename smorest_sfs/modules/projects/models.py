#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
    smorest_sfs.modules.projects.models
    ~~~~~~~~~~~~~~~~~~~~~~~~~

    项目的ORM模块
"""
from sqlalchemy import Column, String

from smorest_sfs.extensions.sqla import Model, SurrogatePK


class Project(Model, SurrogatePK):
    """
    项目

    :attr name: str(128) 项目名称
    """

    __tablename__ = "projects"

    name = Column(String(length=128), nullable=False, doc="项目名称")

    def __repr__(self) -> str:
        return self.name
