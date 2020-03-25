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
    app.extensions.config
    ~~~~~~~~~~~~~~~~~~~~~~~~

    config模块

    源自：Flask-Environment
    由于pytoml已经不再支持以及源码不长故在重新在本地实现

    使用：
    >>> from flask import Flask as BaseFlask
    >>> from app.config import Config
    >>> class Flask(BaseFlask):
            config_class = Config
    >>> app = Flask('test')
    >>> app.config.from_toml('/path/to/toml_file')
"""

import os
from typing import Dict

import toml

from flask.config import Config as FlaskConfig


class Config(FlaskConfig):
    def __init__(self, root_path: str = None, defaults: Dict = None):
        super().__init__(root_path, defaults)

    def from_toml(self, filename: str) -> bool:
        """Updates the values in the config from a TOML file. This function
        behaves as if the TOML object was a dictionary and passed to the
        :param filename: the filename of the JSON file.  This can either be an
                         absolute filename or a filename relative to the
                         root path.
        """

        # Prepeend the root path is we don't have an absolute path
        filename = (
            os.path.join(self.root_path, filename)
            if filename.startswith(os.sep)
            else filename
        )

        try:
            with open(filename) as toml_file:
                obj = toml.load(toml_file)
        except IOError as e:
            e.strerror = "Unable to load configuration file (%s)" % e.strerror
            raise

        return self.from_mapping(obj)
