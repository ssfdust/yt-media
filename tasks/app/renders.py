#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
import sys
from pathlib import Path
from typing import List, Dict
from tasks.app.config import Config
from tasks.app.consts import CONFIG_PATH, NGINX_PATH, SQL_PATH

log = logging.getLogger(__name__)  # pylint: disable=invalid-name

try:
    import jinja2
except ImportError as e:
    log.critical("缺少%s模块，请通过`pip install %s`安装", e.name, e.name)
    sys.exit(1)


class Render:
    def __init__(
        self, loader_path: str, template_and_paths: List[str], config: Dict
    ):
        self.loader_path = loader_path
        self.config = config
        self.env = jinja2.Environment(
            autoescape=True, loader=jinja2.FileSystemLoader(self.loader_path)
        )
        self.template_and_paths = template_and_paths

    def render(self):
        for template_name, config_path in self.template_and_paths:
            template = self.env.get_template(template_name)
            template.stream(**self.config).dump(config_path)


def render_config_to_toml(configs: Config):
    for config_type, config in configs.config_types.items():
        log.info("正在生成 %s 配置...", config_type)
        template_and_paths_list = [
            ["config.template", CONFIG_PATH.format(config=config_type)],
            ["nginx.template", NGINX_PATH.format(config=config_type)],
            ["sql.template", SQL_PATH.format(config=config_type)],
        ]

        render = Render(
            "tasks/app/templates/configurations",
            template_and_paths_list,
            config,
        )
        render.render()

        print()


def render_config_to_dockercompose(configs: Config):
    render = Render(
        "tasks/app/templates/configurations",
        ["docker-compose.yml.template", "docker-compose.yml"],
        configs.production_config,
    )
    render.render()


def render_crud_modules(module_name: str, config: Dict):
    module_path = Path("app/modules/%s" % module_name)

    if module_path.exists():
        log.critical("模块 `%s` 已存在.", module_name)
        sys.exit(1)

    module_path.mkdir(parents=True)

    template_and_paths_list = [
        [
            "%s.py.template" % template_file,
            "%s/%s.py" % (module_path, template_file),
        ]
        for template_file in (
            "__init__",
            "models",
            "params",
            "resources",
            "schemas",
        )
    ]
    render = Render(
        "tasks/app/templates/crud_module", template_and_paths_list, config
    )
    render.render()
