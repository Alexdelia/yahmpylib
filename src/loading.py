from math import ceil
from os import get_terminal_size
from time import time
from typing import Generator, Iterable, List, Optional, TypeVar, Union

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
    if not w or w < 0:
        w = get_terminal_size().columns - (SIZE - w if w else SIZE)
    if w < 3:
        w = 3

    size = 0
    for _ in it:
        size += 1

    if size <= 1:
        for item in it:
            yield item
        return size

    if msgs:
        m: Union[List[str], None] = list(msgs)
        if len(m) != size:
            m = None
    else:
        m = None

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

        if m:
            print(f"\t\033[1m{m[i]}", end="\033[0m", flush=True)

        yield item

    print()
    return size
