from .spec import DEFAULT_REQUEST_BODY_CONTENT_TYPE as DEFAULT_REQUEST_BODY_CONTENT_TYPE
from .utils import deepupdate as deepupdate
from apispec.core import APISpec as APISpec
from marshmallow.schema import SchemaMeta as SchemaMeta
from typing import Any, Callable, Dict, Optional

class ArgumentsMixin:
    ARGUMENTS_PARSER: Any = ...
    def arguments(
        self,
        schema: SchemaMeta,
        *,
        location: str = ...,
        content_type: Optional[str] = ...,
        required: bool = ...,
        description: Optional[str] = ...,
        example: Optional[Dict[str, int]] = ...,
        examples: Optional[Dict[str, Dict[str, int]]] = ...,
        **kwargs: Any
    ) -> Callable: ...
