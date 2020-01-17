# encoding: utf-8
# pylint: disable=invalid-name,unused-argument,too-many-arguments
"""
数据库操作相关Invoke模块

Forked from frol/flask-restplus-server-example
"""
import argparse
import logging
import os

from ._utils import app_context_task

log = logging.getLogger(__name__)  # pylint: disable=invalid-name

try:
    from alembic import __version__ as __alembic_version__
    from alembic.config import Config as AlembicConfig
    from alembic import command
except ImportError:
    log.warning(
        "Alembic can't be imported, some app.db.* tasks won't be available!"
    )
else:

    alembic_version = tuple(
        [int(v) for v in __alembic_version__.split(".")[0:3]]
    )

    class Config(AlembicConfig):
        """
        自定义配置
        """

        def get_template_directory(self):
            package_dir = os.path.abspath(os.path.dirname(__file__))
            return os.path.join(package_dir, "db_templates")


def _get_config(directory, x_arg=None, opts=None):
    """
    预准备AlembicConfig实例
    """
    config = Config(os.path.join(directory, "alembic.ini"))
    config.set_main_option("script_location", directory)
    if config.cmd_opts is None:
        config.cmd_opts = argparse.Namespace()
    for opt in opts or []:
        setattr(config.cmd_opts, opt, True)
    if x_arg is not None:
        if not getattr(config.cmd_opts, "x", None):
            setattr(config.cmd_opts, "x", [x_arg])
        else:
            config.cmd_opts.x.append(x_arg)
    return config


@app_context_task(
    help={"directory": "迁移脚本目录", "multidb": "迁移复数个数据库",}
)
def init(context, directory="migrations", multidb=False):
    """初始化迁移脚本"""
    config = Config()
    config.set_main_option("script_location", directory)
    config.config_file_name = os.path.join(directory, "alembic.ini")
    if multidb:
        command.init(config, directory, "flask-multidb")
    else:
        command.init(config, directory, "flask")


@app_context_task(
    help={
        "rev_id": "手动指定revision id",
        "version_path": "Specify specific path from config for version file",
        "branch_label": "Specify a branch label to apply to the new revision",
        "splice": "Allow a non-head revision as the 'head' to splice onto",
        "head": "选择一个revision <branchname>@head to base new revision on",
        "sql": "显示待执行的Sql语句",
        "directory": "迁移脚本目录",
    }
)
def migrate(
    context, directory="migrations", message=None, sql=False,
):
    """'revision --autogenerate'的简写"""
    config = _get_config(directory, opts=["autogenerate"])
    command.revision(config, message, autogenerate=True, sql=sql)


@app_context_task(help={"revision": "revision标志", "directory": "迁移脚本目录"})
def edit(context, revision="current", directory="migrations"):
    """编辑一个迁移脚本"""
    config = _get_config(directory)
    command.edit(config, revision)


@app_context_task(
    help={
        "tag": "Arbitrary 'tag' name - can be used by custom env.py scripts",
        "sql": "显示待执行的Sql语句",
        "revision": "revision标志",
        "directory": "迁移脚本目录",
        "x_arg": "经由自定义env.py脚本处理的额外参数",
    }
)
def upgrade(
    context,
    directory="migrations",
    revision="head",
    sql=False,
    tag=None,
    x_arg=None,
):
    """更新下一个数据库版本"""
    config = _get_config(directory, x_arg=x_arg)
    command.upgrade(config, revision, sql=sql, tag=tag)


@app_context_task(
    help={
        "tag": "Arbitrary 'tag' name - can be used by custom env.py scripts",
        "sql": "显示待执行的Sql语句",
        "revision": "revision标志",
        "directory": "迁移脚本目录",
        "x_arg": "经由自定义env.py脚本处理的额外参数",
    }
)
def downgrade(
    context,
    directory="migrations",
    revision="-1",
    sql=False,
    tag=None,
    x_arg=None,
):
    """回退到上一个数据哭版本"""
    config = _get_config(directory, x_arg=x_arg)
    if sql and revision == "-1":
        revision = "head:-1"
    command.downgrade(config, revision, sql=sql, tag=tag)
