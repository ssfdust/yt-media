"""
    smorest_sfs.modules.logs.resource
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    日志的资源模块
"""
from typing import Dict, List

from flask.views import MethodView
from flask_jwt_extended import current_user
from flask_sqlalchemy import BaseQuery
from loguru import logger

from smorest_sfs.extensions.api.decorators import paginate
from smorest_sfs.extensions.marshal.bases import (
    BaseIntListSchema,
    BaseMsgSchema,
    GeneralLikeArgs,
)
from smorest_sfs.modules.auth import PERMISSIONS
from smorest_sfs.modules.auth.decorators import doc_login_required, permission_required

from . import blp, models, schemas


@blp.route("/log-details")
class LogView(MethodView):
    @doc_login_required
    @permission_required(PERMISSIONS.LogQuery)
    @blp.arguments(schemas.LogSchema, location="query", as_kwargs=True)
    @blp.response(schemas.LogPageSchema)
    @paginate()
    def get(self, module: str, level: str) -> BaseQuery:
        # pylint: disable=unused-argument
        """
        获取所有日志信息——分页
        """
        query = models.Log.query
        if module or level:
            query = query.filter_like_by(name=name)

        return query


@blp.route("/responselog-details")
class ResponseLogView(MethodView):
    @doc_login_required
    @permission_required(PERMISSIONS.LogQuery)
    @blp.arguments(GeneralLikeArgs, location="query", as_kwargs=True)
    @blp.response(schemas.LogPageSchema)
    @paginate()
    def get(self, name: str) -> BaseQuery:
        # pylint: disable=unused-argument
        """
        获取所有日志信息——分页
        """
        query = models.Log.query
        if name:
            query = query.filter_like_by(name=name)

        return query
