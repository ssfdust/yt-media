#!/usr/bin/env python
# -*- coding: utf-8 -*-


from typing import Dict, Tuple, Union
from flask import Flask

def init_app(app: Flask) -> None:
    from sqlalchemy.orm.exc import NoResultFound
    @app.errorhandler(NoResultFound)
    def handler_no_result(error: Exception) -> Tuple[Dict[str, Union[str, int]], int]:
        return {"code": 404, "msg": "项目不存在"}, 404
