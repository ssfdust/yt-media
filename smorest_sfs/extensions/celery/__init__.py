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
    smorest_sfs.extensions.celery
    ~~~~~~~~~~~~~~~~~~~~~~

    celery模块
"""
from typing import Any, Callable, Optional

import celery
from celery.signals import task_postrun, task_prerun, worker_process_init
from flask import Flask, current_app

def _check_context() -> bool:
    if hasattr(current_app, "name"):
        return True
    return False


class Celery:
    def __init__(self, app: Optional[Flask] = None):
        # we create the celery immediately as otherwise NOTHING WORKS
        self.app = app
        self.context = None
        self.celery = celery.Celery(__name__)
        if app:
            self.init_app(app)

    def init_app(self, app: Flask) -> None:
        self.app = app
        new_celery = celery.Celery(
            app.name + "-Celery",
            broker=app.config["CELERY_BROKER_URL"],
            backend=app.config["CELERY_RESULT_BACKEND"],
        )
        # XXX(dcramer): why the hell am I wasting time trying to make Celery work?
        self.celery.__dict__.update(vars(new_celery))
        self.celery.conf.update(app.config)

        worker_process_init.connect(self._worker_process_init)

        task_postrun.connect(self._task_postrun)
        task_prerun.connect(self._task_prerun)

    def task(self, name: str, *args: Any, **kwargs: Any) -> Callable[..., Any]:
        if not name:
            raise ValueError(
                "Tasks must have a name specified. Recommend: zeus.[task-name]"
            )
        return self.celery.task(name=name, *args, **kwargs)


    @property
    def tasks(self) -> Any:
        return self.celery.tasks

    def call(self, task_name: str, *args: Any, **kwargs: Any) -> Any:
        return self.tasks[task_name](*args, **kwargs)

    def delay(self, task_name: str, *args: Any, **kwargs: Any) -> Any:
        return self.tasks[task_name].delay(*args, **kwargs)

    def get_celery_app(self) -> celery.Celery:
        return self.celery

    def _worker_process_init(self, **_: Any) -> None:
        if self.app and not _check_context():
            self.app.app_context().push()

    def _task_prerun(self, task: Any, **_: Any) -> None:
        if self.app is None or _check_context():
            return

        context = task._flask_context = [
            self.app.app_context(),
            self.app.test_request_context(),
        ]
        for ctx in context:
            ctx.push()

    def _task_postrun(self, task: Any, **_: Any) -> None:
        try:
            context = getattr(task, "_flask_context")
        except AttributeError:
            return

        for ctx in context:
            ctx.pop()
