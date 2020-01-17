# encoding: utf-8
"""
与用户相关的Invoke模块
"""
import getpass

from tasks.app._utils import app_context_task

#  from app.extensions import bcrypt
#
#  pw_hash = bcrypt.generate_password_hash(self.password).decode('utf-8')


class UserFactory:
    def __init__(self, username, email, is_admin, is_active):
        self.username = username
        self.email = email
        self.is_admin = is_admin
        self.is_active = is_active
        self.password = None
        self.avator_info = None
        self.prepare_opts()
        self.get_password()

    def prepare_opts(self):
        from app.modules.auth import ROLES

        if self.is_admin:
            self.avator_info = "Admin"
            self.rolename = ROLES.SuperUser
        else:
            self.avator_info = "Default"
            self.rolename = ROLES.User

    def get_password(self):
        if not self.password:
            self.password = getpass.getpass("请输入密码")

    def create_user(self):
        from app.modules.auth.models import User

        user = User(
            username=self.username, email=self.email, active=self.is_active,
        )
        user.password = self.password
        user.create_userinfo(avator_info=self.avator_info)
        user.set_roles(self.rolename)
        user.save()


@app_context_task(
    help={
        "username": "用户名",
        "email": "用户邮箱",
        "is-admin": "是否admin（默认：是）",
        "is-active": "启用（默认：是）",
    }
)
def create_user(context, username, email, is_admin=True, is_active=True):
    # pylint: disable=unused-argument
    """
    新建用户
    """
    factory = UserFactory(
        username, email, is_admin=is_admin, is_active=is_active
    )
    factory.create_user()
