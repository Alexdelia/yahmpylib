from typing import Any, TypeVar

K = TypeVar('K')
V = TypeVar('V')


def kwargs_exclude(exclude: list[V], **kwargs) -> dict[str, V]:
    return {k: v for k, v in kwargs.items() if k not in exclude}


def dict_exclude(exclude: list[V], d: dict[K, V]) -> dict[K, V]:
    return {k: v for k, v in d.items() if k not in exclude}


def kwargs_exclude_none(**kwargs) -> dict[str, Any]:
    return {k: v for k, v in kwargs.items() if v is not None}


def dict_exclude_none(d: dict[K, V]) -> dict[K, V]:
    return {k: v for k, v in d.items() if v is not None}


def kwargs_exclude_evalfalse(**kwargs) -> dict[str, Any]:
    return {k: v for k, v in kwargs.items() if v}


def dict_exclude_evalfalse(d: dict[K, V]) -> dict[K, V]:
    return {k: v for k, v in d.items() if v}
