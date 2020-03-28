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

from typing import Any

from smorest_sfs.modules.storages.models import Storages
from smorest_sfs.utils.storages import delete_from_rel_path


class StorageFactory:
    def __init__(self, storage: Storages):
        self.storage = storage

    def save(self, commit: bool = True):
        self.storage.save_store()
        return self.storage.save(commit)

    def update(self, commit: bool = True, **kwargs: Any):
        self.storage.store = kwargs.get("store", self.storage.store)
        self.storage.save_store()
        return self.storage.update(commit=commit, **kwargs)

    def hard_delete(self, commit: bool = True):
        delete_from_rel_path(self.storage.path)
        self.storage.hard_delete(commit)
