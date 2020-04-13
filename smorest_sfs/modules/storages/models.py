"""
    smorest_sfs.modules.storages.models
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    文件管理ORM模块
"""
from typing import Any

from smorest_sfs.extensions.sqla import Model, SurrogatePK, db

from .mixin import FileStorage, StoragesMixin


class Storages(StoragesMixin, Model, SurrogatePK):
    """
    文件管理表

    :param          name: str(256)                  文件名
    :param          filetype: str(256)              文件类型
    :param          storetype: str(256)             存储类型
    :param          saved: bool                     是否保存
    :param          path: str(2000)                 保存路径
    :param          uid: int                        用户ID
    :param          _store: FileStorage             文件
    """

    uid = db.Column(db.Integer, doc="用户ID")

    def __init__(self, store: FileStorage, **kwargs: Any):
        self.store = store
        db.Model.__init__(self, **kwargs)  # type: ignore
