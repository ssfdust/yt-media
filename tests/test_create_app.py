# encoding: utf-8
"""
测试创建APP

来源：https://github.com/frol/flask-restplus-server-example/
"""
import pytest
from _pytest.monkeypatch import MonkeyPatch

from smorest_sfs.factory import CONFIG_MAPPGING, create_app
from loguru import logger

ENABLED_MODULES = ["users"]


def test_create_app() -> None:
    app = create_app(ENABLED_MODULES)
    logger.remove(app.extensions['logger_ext'].handler_id)


@pytest.mark.parametrize("flask_config_name", ["development", "testing"])
def test_create_app_passing_config_name(flask_config_name: str) -> None:
    app = create_app(ENABLED_MODULES, flask_config_name)
    logger.remove(app.extensions['logger_ext'].handler_id)


@pytest.mark.parametrize("flask_config_name", ["development", "testing"])
def test_create_app_passing_FLASK_ENV_env(
    monkeypatch: MonkeyPatch, flask_config_name: str  # type: ignore
) -> None:
    monkeypatch.setenv("FLASK_ENV", flask_config_name)
    app = create_app(ENABLED_MODULES)
    logger.remove(app.extensions['logger_ext'].handler_id)


def test_create_app_with_non_existing_config() -> None:
    with pytest.raises(KeyError):
        create_app(ENABLED_MODULES, "non-existing-config")


def test_create_app_with_broken_config() -> None:
    CONFIG_MAPPGING["broken-import-config"] = "broken-import-config"
    with pytest.raises(FileNotFoundError):
        create_app(ENABLED_MODULES, "broken-import-config")
    del CONFIG_MAPPGING["broken-import-config"]
