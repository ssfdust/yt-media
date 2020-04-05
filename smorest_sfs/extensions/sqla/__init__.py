"""
    app.extensions.sqla
    ~~~~~~~~~~~~~~~~~~~~~~~~~~
    拓展Flask-SQLAlchemy模块

    新增软删除功能
    新增对象CRUD功能

    核心部分从一个flask-restful项目中摘录出来，现在已经找不到了
"""

from .surrogatepk import SurrogatePK
from .errors import CharsTooLong, DuplicateEntry
from .model import Model
from .db_instance import db
