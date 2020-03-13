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
    app.factory
    ~~~~~~~~~~~~~~~~~~~~~

    工厂模块

    用以提供库的初始化函数以及注册模块
"""
import os
from typing import List, NoReturn

from loguru import logger

from .extensions import init_app
from .extensions.flask import Flask

CONFIG_MAPPGING = {
    "development": "config/development.toml",
    "production": "config/production.toml",
    "testing": "config/testing.toml",
}


def create_app(modules: List[str], config_name: str = "development") -> Flask:
    """
    创建app工厂

    :param              modules: list               启用模块列表
    :param              config_name: str            配置名称

    ```modules``` 启用的模块列表，模块名必须在app.modules下存在，
    将会按照顺序导入模块。

    ```config_name``` 配置名称，启用的配置名称，存在development,
    production, testing三种配置，从app/config下引用对应的TOML
    配置文件，默认是development配置。
    通过环境变量export FLASK_ENV可以覆盖掉默认的配置信息，在Docker中
    比较好用。
    """
    app = Flask(__name__)

    config_type = os.environ.get("FLASK_ENV", config_name)

    app.config.from_toml(CONFIG_MAPPGING[config_type])

    logger.info(f"Server Started. Server name: {app.config['SERVER_NAME']}")

    app.config["ENABLED_MODULES"] = modules

    init_app(app)

    register_modules(app)

    return app


def register_modules(app: Flask) -> NoReturn:
    """
    注册模块

    为Flask实例注册项目的主要模块
    """
    from . import modules

    # socketio.init_module()
    modules.init_app(app)
