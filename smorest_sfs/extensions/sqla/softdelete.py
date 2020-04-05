"""
    smorest_sfs.extensions.sqla.softdelete
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    软删除模块
"""
from typing import Any, Union
from flask_sqlalchemy import BaseQuery
from sqlalchemy.orm.base import _entity_descriptor
from .db_instance import db


class QueryWithSoftDelete(BaseQuery):
    """
    软删除模块

    根据deleted字段来决定是否显示此对象
    """

    _with_deleted = False

    def __new__(cls, *args: Any, **kwargs: Any) -> db.Model:
        obj = super(QueryWithSoftDelete, cls).__new__(cls)
        obj._with_deleted = kwargs.pop("_with_deleted", False)
        if len(args) > 0:
            super(QueryWithSoftDelete, obj).__init__(*args, **kwargs)
            return obj.filter_by(deleted=False) if not obj._with_deleted else obj
        return obj

    def __init__(self, *args: Any, **kwargs: Any):  # pylint: disable=W0231
        pass

    def with_deleted(self) -> BaseQuery:
        # pylint: disable=C0116
        return self.__class__(
            db.class_mapper(self._mapper_zero().class_),
            session=db.session(),
            _with_deleted=True,
        )

    def _get(self, ident: Any) -> Union[db.Model, None]:
        """提供原本的get方法"""
        return super(QueryWithSoftDelete, self).get(ident)

    def get(self, ident: Any) -> Union[db.Model, None]:
        obj = self.with_deleted()._get(ident)  # pylint: disable=W0212
        return obj if obj is None or self._with_deleted or not obj.deleted else None

    def filter_like_by(self, **kwargs: Any) -> BaseQuery:
        """like方法"""
        clauses = [
            _entity_descriptor(self._joinpoint_zero(), key).like("%{}%".format(value))
            for key, value in kwargs.items()
        ]
        return self.filter(*clauses)
