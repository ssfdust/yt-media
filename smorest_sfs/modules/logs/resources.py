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


@blp.route("/options")
class LogListView(MethodView):
    @doc_login_required
    @permission_required(PERMISSIONS.LogQuery)
    @blp.response(schemas.LogListSchema)
    def get(self) -> Dict[str, List[models.Log]]:
        # pylint: disable=unused-argument
        """
        获取所有日志选项信息
        """
        query = models.Log.query

        items = query.all()

        return {"data": items}


@blp.route("")
class LogView(MethodView):
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

    @doc_login_required
    @permission_required(PERMISSIONS.LogAdd)
    @blp.arguments(schemas.LogSchema)
    @blp.response(schemas.LogItemSchema)
    def post(self, log: models.Log) -> Dict[str, models.Log]:
        # pylint: disable=unused-argument
        """
        新增日志信息
        """
        log.save()
        logger.info(f"{current_user.username}新增了日志{log}")

        return {"data": log}

    @doc_login_required
    @permission_required(PERMISSIONS.LogDelete)
    @blp.arguments(BaseIntListSchema, as_kwargs=True)
    @blp.response(BaseMsgSchema)
    def delete(self, lst: List[int]) -> None:
        # pylint: disable=unused-argument
        """
        批量删除日志
        -------------------------------
        :param lst: list 包含id列表的字典
        """

        models.Log.delete_by_ids(lst)
        logger.info(f"{current_user.username}删除了日志{lst}")


@blp.route(
    "/<int:log_id>",
    parameters=[{"in": "path", "name": "log_id", "description": "日志id"}],
)
class LogItemView(MethodView):
    @doc_login_required
    @permission_required(PERMISSIONS.LogEdit)
    @blp.arguments(schemas.LogSchema)
    @blp.response(schemas.LogItemSchema)
    def put(self, log: models.Log, log_id: int) -> Dict[str, models.Log]:
        """
        更新日志
        """

        log = models.Log.update_by_id(log_id, schemas.LogSchema, log)
        logger.info(f"{current_user.username}更新了日志{log.id}")

        return {"data": log}

    @doc_login_required
    @permission_required(PERMISSIONS.LogDelete)
    @blp.response(BaseMsgSchema)
    def delete(self, log_id: int) -> None:
        """
        删除日志
        """
        models.Log.delete_by_id(log_id)
        logger.info(f"{current_user.username}删除了日志{log_id}")

    @doc_login_required
    @permission_required(PERMISSIONS.LogQuery)
    @blp.response(schemas.LogItemSchema)
    def get(self, log_id: int) -> Dict[str, models.Log]:
        # pylint: disable=unused-argument
        """
        获取单条日志
        """
        log = models.Log.get_by_id(log_id)

        return {"data": log}
