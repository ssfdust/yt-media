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

from smorest_sfs.services.users.userinfo import handle_avator
from smorest_sfs.modules.storages.models import GarbageStorages, StoragesMixin

from smorest_sfs.utils.storages import delete_from_rel_path, save_storage_to_path


class ExtraArgsHandler(object):
    def __init__(self, storage, args):
        self.storage = storage
        self.args = args

    def handle(self):
        func = self.__mapping__.get(self.storage.storetype, None)
        func(self.args)

    __mapping__ = {"avator": handle_avator}


class StorageFactory:
    def __init__(self, storage: StoragesMixin):
        self.storage = storage

    def save(self, commit=True):
        self.storage.save_store()
        return self.storage.save(commit)

    def update(self, commit=True, **kwargs):
        GarbageStorages.create(
            path=self.storage.path,
            storetype=self.storage.storetype,
            storage_id=self.storage.id,
        )
        self.storage.store = kwargs.get("store", self.storage.store)
        self.storage.save_store()
        return self.storage.update(commit=commit, **kwargs)

    def hard_delete(self, commit=True):
        delete_from_rel_path(self.storage.path)
        self.storage.hard_delete()
