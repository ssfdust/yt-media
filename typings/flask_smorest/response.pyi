from .compat import MARSHMALLOW_VERSION_MAJOR as MARSHMALLOW_VERSION_MAJOR
from .spec import DEFAULT_RESPONSE_CONTENT_TYPE as DEFAULT_RESPONSE_CONTENT_TYPE
from .utils import (
    deepupdate as deepupdate,
    get_appcontext as get_appcontext,
    prepare_response as prepare_response,
    set_status_and_headers_in_response as set_status_and_headers_in_response,
    unpack_tuple_response as unpack_tuple_response,
)
from apispec.core import APISpec as APISpec
from marshmallow.schema import SchemaMeta as SchemaMeta
from typing import Any, Callable, Dict, Optional

class ResponseMixin:
    def response(
        self,
        schema: Optional[SchemaMeta] = ...,
        *,
        code: int = ...,
        description: Optional[str] = ...,
        example: Optional[Dict[str, str]] = ...,
        examples: Optional[Dict[str, Dict[str, Any]]] = ...,
        headers: Optional[Dict[str, Dict[str, str]]] = ...
    ) -> Callable: ...
