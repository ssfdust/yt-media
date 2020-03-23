from typing import Mapping, List, Optional, NoReturn

from smorest_sfs.modules.users.models import User, Role, Permission, db, Model
from smorest_sfs.modules.auth.permissions import DEFAULT_ROLES_PERMISSIONS_MAPPING, ROLES, PERMISSIONS


def create_item_from_cls(model_cls: Model, cls: object):
    names = [getattr(cls, attr) for attr in dir(cls) if not attr.startswith('__')]
    db.session.add_all([model_cls(name=name) for name in names])
    db.session.commit()
        

def init_permission():
    create_item_from_cls(Role, ROLES)
    create_item_from_cls(Permission, PERMISSIONS)
    for role, permissions in DEFAULT_ROLES_PERMISSIONS_MAPPING.items():
        permission_instances = Permission.query.filter(
            Permission.name.in_(permissions)
        ).all()
        role_instance = Role.query.filter_by(name=role).first()
        role_instance.permissions = permission_instances
        db.session.add(role_instance)
    db.session.commit()


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
