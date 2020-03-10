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
    新增对象CRUD功能

    核心部分从一个flask-restful项目中摘录出来，现在已经找不到了
"""

from .surrogatepk import SurrogatePK
from .errors import CharsTooLong, DuplicateEntry
from .model import Model
from .db_instance import db
