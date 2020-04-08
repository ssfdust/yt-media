from flask_smorest.fields import Upload as Upload
from marshmallow.fields import Integer as Integer, String as String
from typing import Any, Dict, Union

def uploadfield2properties(
    self, field: Union[Dict, Integer, String], **kwargs: Any
) -> Dict: ...
