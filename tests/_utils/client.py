#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
from typing import Any, Dict, Mapping, List
from collections import OrderedDict
from contextlib import contextmanager

from flask import Response
from flask.testing import FlaskClient
from werkzeug.utils import cached_property

from smorest_sfs.modules.users.models import User


class JSONResponse(Response):
    """
    A Response class with extra useful helpers, i.e. ``.json`` property.

    来源：https://github.com/frol/flask-restplus-server-example/
    """

    # pylint: disable=too-many-ancestors

    @cached_property
    def json(self) -> Dict:
        return json.loads(self.get_data(as_text=True), object_pairs_hook=OrderedDict)


from typing import Union


class AutoAuthFlaskClient(FlaskClient):
    """
    A helper FlaskClient class with a useful for testing ``login`` context
    manager.
    """

    def __init__(self, *args: Any, **kwargs: Any):
        super(AutoAuthFlaskClient, self).__init__(*args, **kwargs)
        self._user: Union[User, None] = None
        self._access_token: Union[str, None] = None
        self._roles: Union[List, None] = None

    @contextmanager
    def login(self, user: User, roles: List[str] = None):
        """
        示例：
            >>> with flask_app_client.login(user, permissions=['SuperUserPrivilege']):
            ...     flask_app_client.get('/api/v1/users/')
        """
        from smorest_sfs.services.auth.auth import login_user, logout_user
        from smorest_sfs.modules.users.models import Role

        self._user = user
        self._roles = roles or []
        self._user.roles = Role.query.filter(Role.name.in_(roles)).all()
        self._user.save()
        if self._user is not None:
            self._access_token = login_user(self._user)["tokens"]["access_token"]
        yield self
        logout_user(self._user)
        self._user.roles = []
        self._user.save()
        self._user = None

    def open(self, *args, **kwargs):
        if self._access_token is not None:
            kwargs = self._combine_headers(**kwargs)

        response = super(AutoAuthFlaskClient, self).open(*args, **kwargs)

        return response

    def _combine_headers(self, **kwargs: Any) -> Any:
        extra_headers = (
            ("Authorization", "Bearer {token}".format(token=self._access_token)),
        )
        if kwargs.get("headers"):
            kwargs["headers"] += extra_headers
        else:
            kwargs["headers"] = extra_headers
        return kwargs
