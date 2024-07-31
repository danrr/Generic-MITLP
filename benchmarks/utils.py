import functools
import sys
import timeit
from operator import add
from typing import Any, Callable, Optional

from consts import NUMBER, REPEAT


def timer[R, **P](f: Callable[P, R], *args: P.args, **kwargs: P.kwargs) -> list[float]:
    return timeit.Timer(functools.partial(f, *args, **kwargs)).repeat(repeat=REPEAT, number=NUMBER)


def timer_with_output[R, **P](f: Callable[P, R], *args: P.args, **kwargs: P.kwargs) -> tuple[list[float], R]:
    output: Optional[R] = None

    def func():
        nonlocal output
        output = f(*args, **kwargs)

    times = timeit.Timer(func).repeat(repeat=REPEAT, number=NUMBER)

    assert output is not None

    return times, output


def get_size(x: Any) -> int:
    size = sys.getsizeof(x)
    if hasattr(x, "__iter__") and not isinstance(x, (str, bytes, bytearray)):
        for y in x:
            size += get_size(y)
    return size


def add_times(a: list[float], b: list[float], *args: list[float]) -> list[float]:
    result = list(map(add, a, b))
    for arg in args:
        result = list(map(add, arg, result))
    return result
