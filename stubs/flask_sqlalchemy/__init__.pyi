from __future__ import annotations
from flask.app import Flask
from datetime import timedelta, datetime
from flask_sqlalchemy.model import DefaultMeta as DefaultMeta, Model as Model
from mypy_extensions import NoReturn as NoReturn
import sqlalchemy as _sa
from sqlalchemy import orm
from sqlalchemy.engine.default import DefaultExecutionContext
from sqlalchemy.engine.base import Connection, Engine
from sqlalchemy.engine.url import URL
from sqlalchemy.orm.mapper import Mapper
from sqlalchemy.orm.relationships import RelationshipProperty
from sqlalchemy.orm.scoping import scoped_session
from sqlalchemy.orm.session import Session as SessionBase, sessionmaker
from sqlalchemy.sql.schema import MetaData, Table
from sqlalchemy.sql.selectable import Select
from sqlite3 import Cursor
from typing import Any, Callable, Dict, Iterator, List, Optional, Tuple, Union

models_committed: Any
before_models_committed: Any

class _DebugQueryTuple(Tuple[str, Tuple[Any, ...], float, float, Any]):
    statement: str = ...
    parameters: Tuple[Any, ...] = ...
    start_time: float = ...
    end_time: float = ...
    context: Any = ...
    @property
    def duration(self) -> float: ...

class SignallingSession(SessionBase):
    app: Any = ...
    def __init__(
        self,
        db: SQLAlchemy,
        autocommit: bool = ...,
        autoflush: bool = ...,
        **options: Any
    ) -> None: ...
    def get_bind(
        self, mapper: Optional[Mapper] = ..., clause: Optional[Select] = ...
    ) -> Engine: ...

class _SessionSignalEvents:
    @classmethod
    def register(cls, session: SessionBase) -> None: ...
    @classmethod
    def unregister(cls, session: SessionBase) -> None: ...
    @staticmethod
    def record_ops(
        session: SessionBase,
        flush_context: Optional[Any] = ...,
        instances: Optional[Any] = ...,
    ) -> None: ...
    @staticmethod
    def before_commit(session: SessionBase) -> None: ...
    @staticmethod
    def after_commit(session: SessionBase) -> None: ...
    @staticmethod
    def after_rollback(session: SessionBase) -> None: ...

class _EngineDebuggingSignalEvents:
    engine: Any = ...
    app_package: Any = ...
    def __init__(self, engine: Engine, import_name: str) -> None: ...
    def register(self) -> None: ...
    def before_cursor_execute(
        self,
        conn: Connection,
        cursor: Cursor,
        statement: str,
        parameters: Tuple[Any, ...],
        context: Any,
        executemany: bool,
    ) -> None: ...
    def after_cursor_execute(
        self,
        conn: Connection,
        cursor: Cursor,
        statement: str,
        parameters: Tuple[Any, ...],
        context: Any,
        executemany: bool,
    ) -> None: ...

def get_debug_queries() -> List[_DebugQueryTuple]: ...

class Pagination:
    query: BaseQuery = ...
    page: int = ...
    per_page: int = ...
    total: int = ...
    items: List[Any] = ...
    def __init__(
        self,
        query: Optional[BaseQuery],
        page: int,
        per_page: int,
        total: Optional[int],
        items: List[Any],
    ) -> None: ...
    @property
    def pages(self) -> int: ...
    def prev(self, error_out: bool = ...) -> Pagination: ...
    @property
    def prev_num(self) -> int: ...
    @property
    def has_prev(self) -> bool: ...
    def next(self, error_out: bool = ...) -> Pagination: ...
    @property
    def has_next(self) -> bool: ...
    @property
    def next_num(self) -> int: ...
    def iter_pages(
        self,
        left_edge: int = ...,
        left_current: int = ...,
        right_current: int = ...,
        right_edge: int = ...,
    ) -> Iterator[int]: ...

class BaseQuery(orm.Query):
    def get_or_404(self, ident: int, description: Optional[str] = ...) -> Any: ...
    def first_or_404(self, description: Optional[str] = ...) -> Any: ...
    def paginate(
        self,
        page: Optional[int] = ...,
        per_page: Optional[int] = ...,
        error_out: bool = ...,
        max_per_page: Optional[int] = ...,
        count: bool = ...,
    ) -> Pagination: ...

class _QueryProperty:
    sa: SQLAlchemy = ...
    def __init__(self, sa: SQLAlchemy) -> None: ...
    def __get__(self, obj: Optional[Any], type: DefaultMeta) -> BaseQuery: ...

class _EngineConnector:
    def __init__(
        self, sa: SQLAlchemy, app: Flask, bind: Optional[str] = ...
    ) -> None: ...
    def get_uri(self) -> str: ...
    def get_engine(self) -> Engine: ...
    def get_options(self, sa_url: URL, echo: bool) -> Dict[str, Any]: ...

def get_state(app: Flask) -> _SQLAlchemyState: ...

class _SQLAlchemyState:
    db: SQLAlchemy = ...
    connectors: Any = ...
    def __init__(self, db: SQLAlchemy) -> None: ...

class SQLAlchemy:
    Query: BaseQuery = ...
    use_native_unicode: Any = ...
    session: SessionBase = ...
    Model: Any = ...
    app: Flask = ...
    def __init__(
        self,
        app: Optional[Flask] = ...,
        use_native_unicode: bool = ...,
        session_options: Optional[Dict[str, Callable[..., Any]]] = ...,
        metadata: Optional[Any] = ...,
        query_class: type = ...,
        model_class: type = ...,
        engine_options: Union[Dict[str, str], Dict[str, type], None] = ...,
    ) -> None: ...
    @property
    def metadata(self) -> MetaData: ...
    def create_scoped_session(
        self, options: Optional[Dict[str, Callable[..., Any]]] = ...
    ) -> scoped_session: ...
    def create_session(self, options: Dict[str, type]) -> sessionmaker: ...
    def make_declarative_base(
        self, model: type, metadata: Optional[Any] = ...
    ) -> DefaultMeta: ...
    def init_app(self, app: Flask) -> None: ...
    def apply_pool_defaults(self, app: Flask, options: Dict[Any, Any]) -> None: ...
    def apply_driver_hacks(
        self, app: Flask, sa_url: URL, options: Dict[str, int]
    ) -> None: ...
    @property
    def engine(self) -> Engine: ...
    def make_connector(
        self, app: Flask = ..., bind: Optional[str] = ...
    ) -> _EngineConnector: ...
    def get_engine(
        self, app: Optional[Flask] = ..., bind: Optional[str] = ...
    ) -> Engine: ...
    def create_engine(self, sa_url: URL, engine_opts: Dict[str, Any]) -> Engine: ...
    def get_app(self, reference_app: Optional[Flask] = ...) -> Flask: ...
    def get_tables_for_bind(self, bind: Optional[str] = ...) -> List[Any]: ...
    def get_binds(self, app: Flask = ...) -> Dict[Any, Engine]: ...
    def create_all(self, bind: str = ..., app: Optional[Flask] = ...) -> None: ...
    def drop_all(self, bind: str = ..., app: Optional[Flask] = ...) -> None: ...
    def reflect(self, bind: str = ..., app: Optional[Flask] = ...) -> None: ...

class _BoundDeclarativeMeta(DefaultMeta):
    def __init__(cls, name: Any, bases: Any, d: Any) -> None: ...

class FSADeprecationWarning(DeprecationWarning): ...
