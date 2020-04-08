from .field_converters import uploadfield2properties as uploadfield2properties
from .plugins import FlaskPlugin as FlaskPlugin
from flask_smorest.exceptions import (
    OpenAPIVersionNotSpecified as OpenAPIVersionNotSpecified,
)
from flask_smorest.utils import prepare_response as prepare_response
from typing import Any, Optional

DEFAULT_REQUEST_BODY_CONTENT_TYPE: str
DEFAULT_RESPONSE_CONTENT_TYPE: str

class DocBlueprintMixin: ...

class APISpecMixin(DocBlueprintMixin):
    def register_converter(
        self, converter: type, conv_type: str, conv_format: Optional[str] = ...
    ) -> None: ...
    def register_field(self, field: type, *args: Any) -> None: ...
