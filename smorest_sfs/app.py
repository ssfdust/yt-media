"""
    smorest_sfs.app
    ~~~~~~~~~~~~~~~~~~~~~~
    实例模块
"""

from .factory import create_app

ENABLED_MODULES = [
    "auth",
    "storages",
    "roles",
    "users",
    "email_templates",
    "codes",
    "projects",
    "menus",
]

app = create_app(ENABLED_MODULES)
