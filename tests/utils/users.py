from typing import Mapping, List, Optional

from smorest_sfs.modules.users.models import User, Role, Permission


class UserManager:
    def __init__(self, user: User, permission_mapping: Mapping[str,
                                                               List[str]]):
        self._user = user
        self._permsssion_mapping = permission_mapping
        self._current_mapping = {}


def generate_user_instance(
    user_id: Optional[int] = None,
    username: Optional[str] = "username",
    phonenum: Optional[str] = None,
    password: Optional[str] = None,
    email: Optional[str] = None,
    is_active: bool = True,
):
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
