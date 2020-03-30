#!/usr/bin/env python
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
    app.extensions.marshal.fields
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    自定义的Marshmallow Filed模块
"""

import pendulum
from flask_babel import get_timezone
from marshmallow import fields
from smorest_sfs.utils.datetime import convert_timezone


class PendulumField(fields.DateTime):
    """
    处理时区
    """

    def _deserialize(self, value, attr, data, **kwargs):
        """将字符串转为arrow类型"""
        if not value:
            raise self.make_error("invalid", input=value, obj_type=self.OBJ_TYPE)

        timezone = get_timezone()
        dt = pendulum.parse(value, tz=timezone)
        return convert_timezone(dt, "utc")

    def _serialize(self, value, attr, obj, **kwargs):
        if value is None:
            return value
        timezone = str(get_timezone())
        value = convert_timezone(pendulum.instance(value), timezone)
        return super()._serialize(value, attr, obj, **kwargs)
