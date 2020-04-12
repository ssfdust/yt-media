from sqlalchemy.util._collections import immutabledict as immutabledict
from typing import Any

PY2: Any

def iteritems(d: Any): ...
def itervalues(d: immutabledict) -> dict_valueiterator: ...

xrange = range
string_types: Any

def to_str(x: str, charset: str = ..., errors: str = ...) -> str: ...
