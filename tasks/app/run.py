# encoding: utf-8
# pylint: disable=too-many-arguments
"""
运行程序相关的Invoke模块
"""

from invoke import task
import logging

log = logging.getLogger(__name__)  # pylint: disable=invalid-name


@task(
    default=True,
    help={
        "host": "主机IP",
        "port": "接口",
        "pty": "pty支持",
        "use-reloader": "是否自动重载（默认：否）",
        "debug": "是否加载Debug（默认：否）",
        "gunicorn": "是否从gunicorn启动（默认：否）",
        "install-dependencies": "是否安装依赖（默认：否）",
    },
)
def server(
    context, bind="127.0.0.1:5000", debug=True, gunicorn=False,
):
    """
    启动服务器
    """
    if gunicorn:
        command = f"gunicorn -b {bind} -k eventlet app.app:app"
        context.run(command, pty=True)
    else:
        host, port = bind.split(":")
        command = f"python run.py -b {host} -p {port}"
        if debug:
            command += " --debug --use-reloader"
        context.run(command, pty=True)
