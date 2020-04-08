from .arguments import ArgumentsMixin as ArgumentsMixin
from .etag import EtagMixin as EtagMixin
from .pagination import PaginationMixin as PaginationMixin
from .response import ResponseMixin as ResponseMixin
from .utils import (
    deepupdate as deepupdate,
    load_info_from_docstring as load_info_from_docstring,
)
from apispec.core import APISpec as APISpec
from flask import Blueprint as FlaskBlueprint
from flask.app import Flask
from typing import Any, Callable, Dict, List, Optional, Union

class Blueprint(
    FlaskBlueprint, ArgumentsMixin, ResponseMixin, PaginationMixin, EtagMixin
):
    HTTP_METHODS: Any = ...
    DEFAULT_LOCATION_CONTENT_TYPE_MAPPING: Any = ...
    DOCSTRING_INFO_DELIMITER: str = ...
    description: Any = ...
    def __init__(self, *args: str, **kwargs: Any) -> None: ...
    def route(
        self,
        rule: str,
        *,
        parameters: Optional[List[Union[Dict[str, str], str]]] = ...,
        **options: Any
    ) -> Callable: ...
    def register_views_in_doc(self, app: Flask, spec: APISpec) -> None: ...
    @staticmethod
    def doc(**kwargs: Any) -> Callable: ...
