#!/usr/bin/env python
# -*- coding: utf-8 -*-
from smorest_sfs.extensions import db
from smorest_sfs.utils.storages import (
    delete_from_rel_path,
    save_storage_to_path,
    load_storage_from_path,
)


class StoragesMixin:

    name = db.Column(db.String(256), nullable=True, doc="文件名")
    filetype = db.Column(db.String(256), nullable=True, doc="文件类型", default="")
    storetype = db.Column(db.String(256), nullable=True, doc="存储类型")
    saved = db.Column(db.Boolean, nullable=True, default=False, doc="是否保存")
    path = db.Column(db.String(2000), nullable=True, doc="文件路径")
    _store = None

    @property
    def store(self):
        if self._store is None and self.saved:
            self._store = load_storage_from_path(self.name, self.path)
        return self._store

    def as_stream(self):
        self._store.stream.seek(0)
        return self._store.stream

    @store.setter
    def store(self, val):
        self._store = val

    def save_store(self):
        """
        存储文件

        每一次存储文件都会生成一个新的地址
        """
        if self.store is not None:
            self.filetype = self.store.content_type
            self.path = save_storage_to_path(self.store, self.storetype)
            self.saved = True
