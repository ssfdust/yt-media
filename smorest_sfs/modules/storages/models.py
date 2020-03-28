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

from loguru import logger

from smorest_sfs.extensions.sqla import Model, SurrogatePK, db
from smorest_sfs.utils.storages import (
    save_storage_to_path,
    load_storage_from_path,
    delete_from_rel_path,
)
from .mixin import StoragesMixin


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

    __trunk_size = 1000

    def __init__(self, **kwargs):
        self.store = kwargs.pop("store", None)
        db.Model.__init__(self, **kwargs)
