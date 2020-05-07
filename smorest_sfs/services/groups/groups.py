#!/usr/bin/env python
# -*- coding: utf-8 -*-
from typing import List

from loguru import logger
from smorest_sfs.modules.users.models import Group
from smorest_sfs.modules.roles.models import Role
from smorest_sfs.plugins.sa import execute
from smorest_sfs.utils.sqla import get_histroy
from .sqls import AddRoleToGroup, DeleteRoleFromGroup

def add_roles_to_group(group: Group, roles: List[Role]) -> None:
    if roles:
        logger.info(f"为组{group.name}添加{', '.join([r.name for r in roles])}角色")
        execute(AddRoleToGroup, group=group, roles=roles)


def delete_roles_from_group(group: Group, roles: List[Role]) -> None:
    if roles:
        logger.info(f"为组{group.name}删除{', '.join([r.name for r in roles])}角色")
        execute(DeleteRoleFromGroup, group=group, roles=roles)


def parse_group_change(group: Group) -> None:
    try:
        hist = get_histroy(group, "roles")
        delete_roles_from_group(group, hist.deleted)
        add_roles_to_group(group, hist.added)
    except ValueError:
        logger.debug(f"There is no changes in roles of group {group.name}")
