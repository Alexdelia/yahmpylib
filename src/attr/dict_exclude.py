from typing import Any, Dict, List, TypeVar

K = TypeVar('K')
V = TypeVar('V')


def kwargs_exclude(exclude: List[V], **kwargs) -> Dict[str, V]:
    return {k: v for k, v in kwargs.items() if k not in exclude}


def dict_exclude(exclude: List[V], d: Dict[K, V]) -> Dict[K, V]:
    return {k: v for k, v in d.items() if k not in exclude}


def kwargs_exclude_none(**kwargs) -> Dict[str, Any]:
    return {k: v for k, v in kwargs.items() if v is not None}


def dict_exclude_none(d: Dict[K, V]) -> Dict[K, V]:
    return {k: v for k, v in d.items() if v is not None}


def kwargs_exclude_evalfalse(**kwargs) -> Dict[str, Any]:
    return {k: v for k, v in kwargs.items() if v}


def dict_exclude_evalfalse(d: Dict[K, V]) -> Dict[K, V]:
    return {k: v for k, v in d.items() if v}
