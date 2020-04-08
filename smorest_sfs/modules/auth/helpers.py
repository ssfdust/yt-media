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
from typing import Dict, Optional
from datetime import datetime

from sqlalchemy.orm.exc import NoResultFound
from flask_jwt_extended import decode_token

from .models import TokenBlackList


def _epoch_utc_to_datetime(epoch_utc: str) -> datetime:
    """
    转换时间戳为日期时间
    """
    return datetime.fromtimestamp(float(epoch_utc))


def is_token_revoked(decoded_token: Dict[str, str]) -> bool:
    """
    从数据库中寻找token是否被撤销
    """
    jti = decoded_token["jti"]
    try:
        token = TokenBlackList.query.filter_by(jti=jti).one()
        return token.revoked
    except NoResultFound:
        return True


def add_token_to_database(
    encoded_token: str,
    identity_claim: str,
    custom_token_type: Optional[str] = None,
    allow_expired: bool = False,
) -> None:
    """
    将新的Token解码后加入到数据库

    :param custom_token_type: 自定义的token类型
    :param identity_claim: 指定的认证字段
    """
    decoded_token = decode_token(encoded_token, allow_expired=allow_expired)
    jti = decoded_token["jti"]
    token_type = decoded_token["type"] if not custom_token_type else custom_token_type
    user_identity = decoded_token[identity_claim]
    expires = _epoch_utc_to_datetime(decoded_token["exp"])
    revoked = False
    TokenBlackList.create(
        jti=jti,
        token_type=token_type,
        user_identity=user_identity,
        expires=expires,
        revoked=revoked,
    )
