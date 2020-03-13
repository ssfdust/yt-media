#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
验证用户登录
"""
from typing import NoReturn, Dict
from contextlib import contextmanager

from flask import current_app
from flask_jwt_extended import create_access_token, create_refresh_token
from flask_smorest import abort
from loguru import logger

from smorest_sfs.extensions.rpcstore.captcha import CaptchaStore
from smorest_sfs.modules.auth.helpers import add_token_to_database
from smorest_sfs.modules.users.models import User
from smorest_sfs.modules.auth.models import TokenBlackList


class UserLoginChecker:
    def __init__(self, user: User, password: str, code: str, token: str):
        self.user = user
        self.password = password
        self.code = code
        self._token = token

    def _check_capture_code(self):
        store = CaptchaStore(self._token)
        code_lst = store.get_captcha()
        if self.code not in code_lst:
            logger.error(f"{self.user.email} 登录时验证码{self.code}错误，\n"
                         f"正确验证码为{code_lst}")
            abort(403, message="验证码错误")

        return True

    def _check_user(self) -> NoReturn:
        if self.user is None:
            logger.warning("登录用户不存在")
            abort(404, message="用户不存在")

        if self.user.active is not True:
            logger.warning(f"{self.user.email} 未激活，尝试登录")
            abort(403, message="用户未激活")

        return True

    def _check_passwd(self):
        if self.user.password != self.password:
            logger.error(f"{self.user.email} 登录密码错误")
            abort(403, message="密码错误")

        return True

    @contextmanager
    def check(self) -> User:
        if self._check_capture_code() and self._check_user(
        ) and self._check_passwd():
            yield self.user


def login_user(user: User) -> Dict[str, Dict[str, str]]:
    """用户登录"""
    # 生成jwt
    access_token = create_access_token(identity=user.email)
    refresh_token = create_refresh_token(identity=user.email)

    # 将token加入数据库
    add_token_to_database(access_token,
                          current_app.config["JWT_IDENTITY_CLAIM"])
    add_token_to_database(refresh_token,
                          current_app.config["JWT_IDENTITY_CLAIM"])

    logger.info(f"{user.email} 登录成功")

    # 组装data
    return {
        "tokens": {
            "refresh_token": refresh_token,
            "access_token": access_token
        }
    }


def logout_user(user: User) -> NoReturn:
    TokenBlackList.query.filter(
        TokenBlackList.user_identity == user.email,
        TokenBlackList.revoked.is_(False)
    ).update({"revoked": True})
