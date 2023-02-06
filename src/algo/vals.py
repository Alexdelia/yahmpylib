from typing import List


def vals(obj: object) -> List[str]:
    return [
        obj.__getattribute__(attr)
        for attr in dir(obj)
        if not attr.startswith('__')
    ]