from math import ceil
from os import get_terminal_size
from time import time
from typing import Generator, Iterable, Optional, TypeVar

T = TypeVar('T')

SIZE = 38


def loading(
    it: Iterable[T],
    w: Optional[int] = None,
    c: str = '█',
    msgs: Optional[Iterable[str]] = None
) -> Generator[T, None, int]:
    """
    Loading bar for iterable objects.

    :param it: Iterable[T]: Iterable object.
    :param w: Optional[int] = None: Width of the bar.
        negative value will let space away from the right side.
    :param c: str = '█': Character to fill the bar.
    :return: Generator[T, None, int]: Generator of the iterable object.
        And return the size of the iterable object.
    """
    w = _reset_w(w)

    size = sum(1 for _ in it)

    if size <= 1:
        for item in it:
            yield item
        return size

    msgs = _validate_msgs(msgs, size)

    start = time()
    for i, item in enumerate(it):
        percent = [i / (size - 1) * 100, 100][i == size - 1]
        bar_w = ceil(i / (size - 1) * w)
        elapsed = time() - start
        eta = elapsed * size / (i + 1) - elapsed

        print(
            f"\033[2K\r\033[1;3;34m{eta:.2f}s\033[0m"
            + f"\t\033[1m[\033[32m{percent:3.0f}%\033[0m\033[1m]"
            + f" [\033[35m{c * bar_w}\033[0m{' ' * (w - bar_w)}\033[1m]"
            + f" \033[3m{i + 1}\033[0m\033[1m/\033[2;3m{size}\033[0m"
            + f"\t\033[1m| \033[1;3;33m{elapsed:.2f}s",
            end="\033[0m"
        )

        if msgs:
            print(f"\t\033[1m{msgs[i]}", end="\033[0m", flush=True)

        yield item

    print()
    return size


def _reset_w(w: Optional[int] = None) -> int:
    """
    Resize the width of the bar.

    :param w: int: Width of the bar.
    :return: int: Resized width of the bar.
    """
    return max(3, get_terminal_size().columns - (SIZE - w if w else SIZE))


def _validate_msgs(
    msgs: Optional[Iterable[str]],
    size: int,
) -> Optional[list[str]]:
    """
    Validate the messages.

    :param msgs: Optional[Iterable[str]]: Messages.
    :return: Optional[list[str]]: Validated messages.
    """
    return list(msgs) if msgs and len(list(msgs)) == size else None
