"""
    smorest_sfs.modules.codes.resource
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    编码的资源模块
"""
from typing import Dict, List

from flask.views import MethodView

from smorest_sfs.modules.auth import PERMISSIONS
from smorest_sfs.modules.auth.decorators import doc_login_required, permission_required

from . import blp, models, schemas


@blp.route("/options")
class CodeListView(MethodView):
    @doc_login_required
    @permission_required(PERMISSIONS.CodeQuery)
    @blp.response(schemas.CodeListSchema)
    def get(self) -> Dict[str, List[models.Code]]:
        # pylint: disable=unused-argument
        """
        获取所有编码选项信息
        """
        query = models.Code.query

        items = query.all()

        return {"data": items}
