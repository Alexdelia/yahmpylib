import re
from ast import literal_eval
from json import dumps
from typing import Any, AnyStr, Optional

from requests import Response
from result import Err, Ok, Result


def bdump(
    json: dict[str, Any] | str | AnyStr | None,
    q: Optional[Response] = None,
) -> str:
    r = _to_str(json)
    if r.is_err():
        return r.unwrap_err()

    r = _eval(r.unwrap(), q)
    if r.is_err():
        return r.unwrap_err()

    return re.sub(
        r'"(detail)"(.*)?"(.*)"', '"\\1"\\2"\033[31;1m\\3\033[0m"',
        re.sub(
            r'\n', "\n\t\t      \t",
            "\n" + dumps(r.unwrap(), indent=4, sort_keys=False)
        )
    )


def _to_str(
    json: dict[str, Any] | str | AnyStr | None
) -> Result[dict[str, Any] | str, str]:
    if json is None or json == "None":
        return Err("\033[34;1mNone\033[0m")

    if isinstance(json, bytes):
        json = json.decode()

    if not json:
        return Err(str(json))

    return Ok(json)


def _eval(
    json: dict[str, Any] | str,
    q: Optional[Response] = None,
) -> Result[Any, str]:
    if isinstance(json, str):
        try:
            json = literal_eval(json)
        except Exception:
            if q:
                r = _try_json(json, q)
                if r.is_err():
                    return r

    return Ok(json) if json else Err(str(json))


def _try_json(
    json: str,
    q: Response,
) -> Result[Any, str]:
    try:
        return Ok(q.json())
    except Exception:
        return Err(json)
