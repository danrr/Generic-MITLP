import functools
import timeit
from typing import Callable, Optional

from consts import NUMBER


def timer[R, **P](f: Callable[P, R], *args: P.args, **kwargs: P.kwargs) -> float:
    return timeit.Timer(functools.partial(f, *args, **kwargs)).timeit(number=NUMBER)


def timer_with_output[R, **P](f: Callable[P, R], *args: P.args, **kwargs: P.kwargs) -> tuple[float, R]:
    output: Optional[R] = None

    def func():
        nonlocal output
        output = f(*args, **kwargs)

    times = timeit.Timer(func).timeit(number=NUMBER)

    assert output is not None

    return times, output
