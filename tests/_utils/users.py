from typing import List, Mapping, NoReturn, Optional

from smorest_sfs.modules.auth.permissions import (
    DEFAULT_ROLES_PERMISSIONS_MAPPING, PERMISSIONS, ROLES)
from smorest_sfs.modules.users.models import Model, Permission, Role, User, db


def generate_user_instance(
        user_id: Optional[int] = None,
        username: Optional[str] = "username",
        phonenum: Optional[str] = None,
        password: Optional[str] = None,
        email: Optional[str] = None,
        is_active: bool = True,
) -> User:
    """
    Returns:
        user_instance (User) - an not committed to DB instance of a User model.
    """

    if password is None:
        password = "%s_password" % username
    user_instance = User(
        id=user_id,
        phonenum=phonenum or "12345678",
        active=is_active,
        username=username,
        email=email or "%s@email.com" % username,
        password=password,
    )
    return user_instance
