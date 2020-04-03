"""
    smorest_sfs.services.storages.handlers
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    文件处理工厂
"""
from typing import Any

from smorest_sfs.modules.storages.models import Storages
from smorest_sfs.utils.storages import delete_from_rel_path


class StorageFactory:
    """文件处理

    文件的CRUD操作
    """

    def __init__(self, storage: Storages):
        self.storage = storage

    def save(self, commit: bool = True) -> Any:
        """文件保存"""
        self.storage.save_store()
        return self.storage.save(commit)

    def update(self, commit: bool = True, **kwargs: Any) -> Any:
        """文件更新"""
        self.storage.store = kwargs.get("store", self.storage.store)
        self.storage.save_store()
        return self.storage.update(commit=commit, **kwargs)

    def hard_delete(self, commit: bool = True) -> None:
        """文件永久删除"""
        delete_from_rel_path(self.storage.path)
        self.storage.hard_delete(commit)
