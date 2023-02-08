import re
from ast import literal_eval
from json import dumps
from sys import stderr
from typing import Any, Callable, Dict, Optional, Union

import requests

LOCAL_API_ADDRESS = "http://127.0.0.1:5000/"


def requester(
    endpoint: str,
    api_address: str = LOCAL_API_ADDRESS,
    method: Callable[[Any], requests.Response] = requests.get,
    params: Optional[Dict[str, Any]] = None,
    data: Optional[Any] = None,
    status_code: int = 200,
) -> requests.Response:
    """
    make request for a given endpoint
        and check the right status code has been thrown

    in case of error, print the request and response
    """
    q: requests.Response = method(
        LOCAL_API_ADDRESS + endpoint, json=data, params=params
    )

    url = re.sub(
        r'=', "\033[34;1;2m=\033[0m",
        re.sub(
            r'(\b/{1}\b|\?|&)', "\n\t\t   \'->\t\033[34;1;2m\\1\033[0m", q.url
        )
    )
    print(
        "\033[31;1mREQUEST RESPONSE\033[0m:",
        "\t\033[34;1mSENT\033[0m:",
        f"\t\t\033[33;1mmethod\033[0m: \t\033[1m{q.request.method}\033[0m",
        f"\t\t\033[33;1murl\033[0m:    \t{url}",
        f"\t\t\033[33;1mbody\033[0m:   \t{_format_flat_json(q.request.body)}",
        f"\t\t\033[33;1mparams\033[0m: \t{_format_flat_json(params)}",
        "\t\033[34;1mRECEIVED\033[0m:",
        "\t\t\033[33;1mcode\033[0m:   \t\033["
        + ['31', '32'][q.status_code == status_code]
        + f";1m{q.status_code}\033[0m"
        + f"\t\033[3m(expected \033[1;3m{status_code}\033[0m\033[3m)\033[0m",
        f"\t\t\033[33;1mcontent\033[0m:\t{_format_flat_json(q.content, q)}",
        "\t\t\033[33;1mtime\033[0m:   \t\033[2;3m"
        + f"{q.elapsed.microseconds / 1e+6}\033[0m\033[1;3ms\033[0m",
        # f"\t\t\033[33;1mheaders\033[0m:\t{_format_flat_json(dict(q.headers))}",
        file=stderr,
        sep="\n"
    )

    assert q.status_code == status_code, f"\
Wrong status code, expected {status_code}, got {q.status_code}\n{q.text}"

    return q


def _format_flat_json(
    json: Union[Dict[str, Any], str, bytes, None],
    q: Optional[requests.Response] = None
) -> str:
    if json and isinstance(json, bytes):
        json = json.decode()

    if json is None or json == "None":
        return "\033[34;1mNone\033[0m"

    if isinstance(json, str) \
            and (json[0] != '{' and json[-1] != '}') \
            and (json[0] != '[' and json[-1] != ']'):
        return f"\033[31;1m{json}\033[0m"

    if isinstance(json, str):
        try:
            json = literal_eval(json)
        except Exception:
            if q:
                try:
                    json = q.json()
                except Exception:
                    return json

    if not json:
        return str(json)

    return re.sub(
        r'"(detail)"(.*)?"(.*)"', '"\\1"\\2"\033[31;1m\\3\033[0m"',
        re.sub(
            r'\n', "\n\t\t      \t",
            "\n" + dumps(json, indent=4, sort_keys=False)
        )
    )
