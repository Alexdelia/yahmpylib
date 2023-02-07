from enum import Enum
from typing import List, Union


def vals(obj: Union[object, type]) -> List[str]:
    """
    returns a list of the values of the attributes of the given object or type

    works with Enum types and instances
    """
    if isinstance(obj, type):
        if issubclass(obj, Enum):
            return [e.value for e in obj]
        obj = obj()

    return [
        obj.__getattribute__(attr)
        for attr in dir(obj)
        if not attr.startswith('__')
    ]