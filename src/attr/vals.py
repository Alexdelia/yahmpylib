from enum import Enum


def vals(obj: object | type) -> list[str]:
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
