#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright 2019 RedLotus <ssfdust@gmail.com>
# Author: RedLotus <ssfdust@gmail.com>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""
    app.extensions.sqla
    ~~~~~~~~~~~~~~~~~~~~~~~~~~
    拓展Flask-SQLAlchemy模块

    新增软删除功能
    新增ArrowType支持
    新增对象CRUD功能

    核心部分从一个flask-restful项目中摘录出来，现在已经找不到了
"""

from datetime import datetime
from .mixin import CRUDMixin
from .db_instance import db
from .softdelete import QueryWithSoftDelete


class Model(CRUDMixin, db.Model):
    """简单的CRUD处理"""

    query_class = QueryWithSoftDelete

    __abstract__ = True


# https://speakerdeck.com/zzzeek/building-the-app


class SurrogatePK:
    """
    数据库表栏目模板

    :attr id: int 主键
    :attr deleted: bool 删除状态
    :attr modified: datetime 修改时间
    :attr created: datetime 创建时间
    """

    id = db.Column(
        db.Integer, primary_key=True, info={"marshmallow": {"dump_only": True}}
    )
    deleted = db.Column(
        db.Boolean,
        nullable=False,
        doc="已删除",
        default=False,
        info={"marshmallow": {"dump_only": True}},
    )
    modified = db.Column(
        db.DateTime(True),
        nullable=False,
        doc="修改时间",
        default=datetime.utcnow(),
        info={
            "marshmallow": {"format": "%Y-%m-%d %H:%M:%S", "dump_only": True}
        },
    )
    created = db.Column(
        db.DateTime(True),
        nullable=False,
        doc="创建时间",
        default=datetime.utcnow(),
        info={
            "marshmallow": {"format": "%Y-%m-%d %H:%M:%S", "dump_only": True}
        },
    )

    @classmethod
    def get_by_id(cls, _id):
        """
        根据ID查询数据库
        """
        with db.session.no_autoflush:
            return cls.query.get_or_404(_id)

    @classmethod
    def delete_by_id(cls, _id, commit=True):
        """
        根据ID删除数据
        """
        item = cls.get_by_id(_id)
        item.delete(commit)

    @classmethod
    def delete_by_ids(cls, ids, commit=True):
        """
        批量删除
        """
        kw = [{"id": id, "deleted": True} for id in ids]
        db.session.bulk_update_mappings(cls, kw)

        if commit:
            db.session.commit()

    @classmethod
    def update_by_id(cls, _id, schema, instance, commit=True):
        """
        根据id，Schema，以及临时实例更新元素

        :param ids: list 主键
        :param schema: Schema Schema类或实例
        :param instance: object 临时Model对象
        :param commit: bool 是否提交

        详见update_by_ma注释
        """
        item = cls.get_by_id(_id)

        item.update_by_ma(schema, instance, commit=commit)

        return item
