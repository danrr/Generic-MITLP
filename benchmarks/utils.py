import functools
import sys
import timeit
from operator import add

from consts import REPEAT, NUMBER


def timer(f, *args):
    return timeit.Timer(functools.partial(f, *args)).repeat(
        repeat=REPEAT,
        number=NUMBER
    )


def get_size(x):
    size = sys.getsizeof(x)
    if hasattr(x, '__iter__') and not isinstance(x, (str, bytes, bytearray)):
        for y in x:
            size += get_size(y)
    return size


def add_times(a, b, *args):
    result = list(map(add, a, b))
    for arg in args:
        result = list(map(add, arg, result))
    return result

