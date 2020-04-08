import werkzeug.exceptions as wexc

class FlaskSmorestError(Exception): ...
class OpenAPIVersionNotSpecified(FlaskSmorestError): ...
class CheckEtagNotCalledError(FlaskSmorestError): ...

class NotModified(wexc.HTTPException, FlaskSmorestError):
    code: int = ...
    description: str = ...

class PreconditionRequired(wexc.PreconditionRequired, FlaskSmorestError):
    description: str = ...

class PreconditionFailed(wexc.PreconditionFailed, FlaskSmorestError): ...
