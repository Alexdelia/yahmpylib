from json import dumps
from typing import Any, Iterable, Optional, Tuple, TypeVar


class EvalTrue:

    def __str__(self) -> str:
        return "\033[0m\033[34;2;1mevaluating to \033[32;2;1mTrue\033[0m"

    def __repr__(self) -> str:
        return "\033[0m\033[34;2;1mevaluating to \033[32;2;1mTrue\033[0m"


class EvalFalse:

    def __str__(self) -> str:
        return "\033[0m\033[34;2;1mevaluating to \033[31;2;1mFalse\033[0m"

    def __repr__(self) -> str:
        return "\033[0m\033[34;2;1mevaluating to \033[31;2;1mFalse\033[0m"


def asrt(got: Any, expected: Any = EvalTrue(), *msg: str) -> Any:
    """
    assert got == expected
    special characters:
        `\\G`: got
        `\\E`: expected
    if expected is not given, do: assert got
    and return got
    """
    if expected is EvalTrue or expected is EvalFalse:
        expected = expected()

    if isinstance(expected, EvalTrue):
        assert got, _asrt_msg(got, expected, *msg)
    elif isinstance(expected, EvalFalse):
        assert not got, _asrt_msg(got, expected, *msg)
    else:
        assert got == expected, _asrt_msg(got, expected, *msg)

    return got


def _asrt_msg(got: Any, expected: Any, *msg: str) -> str:
    e = ("\n" + dumps(expected, indent=4)).replace("\n", "\n\033[32;1m") \
        if isinstance(expected, dict) \
        else str(expected)

    g = ("\n" + dumps(got, indent=4)).replace("\n", "\n\033[31;1m") \
        if isinstance(got, dict) \
        else str(got)

    m = ''.join(msg).replace(r'\G', g).replace(r'\E', e)

    g += _asrt_msg_missing_extra(got, expected) or ''

    return "\033[0m\033[1m" + \
        m \
        + f"\n\033[0m\t\033[1mexpected: \033[32;1m{e}" \
        + f"\n\033[0m\t\033[1mgot: \033[31;1m{g}\033[0m"


def _asrt_msg_missing_extra(got: Any, expected: Any) -> Optional[str]:
    if not ((isinstance(got, dict) and isinstance(expected, dict)) or
            (hasattr(got, "__iter__") and hasattr(expected, "__iter__"))):
        return None

    if isinstance(got, dict) and isinstance(expected, dict):
        missing, extra = _diff_set(
            got.keys(),
            expected.keys(),
            {
                **got,
                **expected
            },
        )
    else:
        missing, extra = _diff_set(got, expected)

    return \
        f"\033[0m\033[1mmissing:\n\033[31;1m{missing}\033[0m" \
        if missing else "" \
        + f"\033[0m\033[1mextra:\n\033[31;1m{extra}\033[0m" \
        if extra else ""


K = TypeVar('K')


def _diff_set(
    got: Iterable[K],
    expected: Iterable[K],
    d: Optional[dict[K, Any]] = None
) -> Tuple[str, str]:
    g = frozenset(got)
    e = frozenset(expected)

    def fv(k: K) -> str:
        if d:
            return "\033[31;1;2m ->\t\033[3m" \
                + d.get(k, '\033[0m\033[35;1;2mKeyError\033')
        return ""

    return (
        '\n'.join(f"\033[31;1m{k}{fv(k)}\033[0m" for k in e - g),
        '\n'.join(f"\033[31;1m{k}{fv(k)}\033[0m" for k in g - e)
    )
