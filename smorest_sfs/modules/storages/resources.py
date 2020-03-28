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

from flask.views import MethodView
from loguru import logger

from smorest_sfs.extensions.marshal.bases import BaseMsgSchema
from smorest_sfs.modules.auth.decorators import doc_login_required, role_required
from smorest_sfs.modules.auth import ROLES
from smorest_sfs.services.storages.handlers import StorageFactory
from smorest_sfs.utils.storages import make_response_from_store

from . import blp, models, schemas


@blp.route("/<int:file_id>")
class StoragesView(MethodView):
    @doc_login_required
    @role_required(ROLES.User)
    @blp.response(code=200, description="获取文件")
    def get(self, file_id):
        """
        获取文件
        """
        storage = models.Storages.get_by_id(file_id)

        return make_response_from_store(storage.store)

    @doc_login_required
    @blp.arguments(schemas.UploadParams(), location="files")
    @role_required(ROLES.User)
    @blp.response(BaseMsgSchema)
    def put(self, args, file_id):
        """
        修改文件
        """
        args["store"] = args.pop("file")
        storage = models.Storages.get_by_id(file_id)
        factory = StorageFactory(storage)
        logger.info(f"修改了文件{storage.name} id: {storage.id}")
        factory.update(**args)

        return {"code": 0, "msg": "success"}

    @doc_login_required
    @blp.response(BaseMsgSchema)
    @role_required(ROLES.User)
    def delete(self, file_id):
        """
        删除文件
        """
        storage = models.Storages.get_by_id(file_id)
        logger.info(f"删除了文件{storage.name} id: {storage.id}")
        storage.delete()

        return {"code": 0, "msg": "success"}


@blp.route("/upload/<storetype>")
class UploadView(MethodView):
    @doc_login_required
    @role_required(ROLES.User)
    @blp.arguments(schemas.UploadParams(), location="files")
    @blp.response(schemas.UploadSchema)
    def post(self, args, storetype: str):
        """
        上传文件
        """
        logger.info(f"上传了文件{args['file'].filename}")
        args["_store"] = args.pop("file")
        factory = StorageFactory(models.Storages(storetype=storetype, **args))
        factory.save()

        return {"code": 0, "msg": "success", "data":{"file_id": factory.storage.id}}
