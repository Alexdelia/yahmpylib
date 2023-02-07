import json
from os.path import dirname, realpath
from typing import Any, Dict, Iterable, Optional

PATH_TO_ROOT = "../"


def scan(
    cls,
    file: str,
    optional_keys: Optional[Iterable[str]] = None,
) -> Dict[str, Any]:
    """
    read file from root repo directory
    validate it against
        cls.schema(by_alias=True).get("properties", dict()).keys()
    and return dict of read json
    """
    d = read(file)
    validate(
        d,
        cls.schema(by_alias=True).get("properties", dict()).keys(),
        file,
        optional_keys,
    )
    return d


def read(file: str) -> Dict[str, Any]:
    return json.load(
        open(f"{dirname(realpath(__file__))}/{PATH_TO_ROOT}{file}", "r")
    )


def validate(
    d: Dict[str, Any],
    keys: Iterable[str],
    file: str,
    optional_keys: Optional[Iterable[str]] = None,
) -> None:
    if optional_keys is None:
        optional_keys = frozenset()

    s = frozenset(keys) - frozenset(optional_keys) - frozenset(d.keys())

    if s:
        raise ValueError(f"{list(s)} is missing from {file}")
