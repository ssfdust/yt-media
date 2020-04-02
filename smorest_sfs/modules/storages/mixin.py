#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
文件Mixin处理模块
"""
from typing import Optional, IO

from smorest_sfs.extensions import db
from smorest_sfs.utils.storages import (FileStorage, load_storage_from_path,
                                        save_storage_to_path)


class StoragesMixin:
    """文件类型Mixin

    支持文件读写以及流操作
    """
    filename: str
    name = db.Column(db.String(256), nullable=True, doc="文件名")
    filetype = db.Column(db.String(256), nullable=True, doc="文件类型", default="")
    storetype = db.Column(db.String(256), nullable=True, doc="存储类型")
    saved = db.Column(db.Boolean, nullable=True, default=False, doc="是否保存")
    path = db.Column(db.String(2000), nullable=True, doc="文件路径")
    _store = None

    @property
    def store(self) -> Optional[FileStorage]:
        """返回文件的FileStorage对象"""
        if self._store is None and self.saved:
            self._store = load_storage_from_path(self.name, self.path)
        return self._store

    @store.setter
    def store(self, val: FileStorage) -> None:
        self._store = val

    def as_stream(self) -> IO[bytes]:
        """文件流形式返回"""
        if self._store is not None:
            self._store.stream.seek(0)
            return self._store.stream
        raise FileNotFoundError("文件不存在")

    def save_store(self) -> None:
        """
        存储文件

        每一次存储文件都会生成一个新的地址
        """
        if self.store is not None:
            self.name = self.store.filename if self.store.filename else self.filename
            self.filetype = self.store.content_type
            self.path = save_storage_to_path(self.store, self.storetype)
            self.saved = True
