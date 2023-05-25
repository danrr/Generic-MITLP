import time

from lib import TLP

from consts import KEYSIZE, SQUARINGS_PER_SEC, SEED
from utils import timer


def now():
    return time.perf_counter_ns()


INTERVAL = 10
MILI_TO_S = 10 ** 9
INTERVAL_NS = INTERVAL * MILI_TO_S


def count_squarings_in_fixed_time():
    tlp = TLP(seed=SEED)
    pk, sk = tlp.setup(1, 1, keysize=KEYSIZE)
    n, _, r = pk

    counter = 0
    start = now()
    stop = start + INTERVAL_NS
    s = SQUARINGS_PER_SEC[KEYSIZE] * INTERVAL
    # use previous value to refine; avoid making more calls to now()
    for _ in range(s - s // 20):
        r = (r ** 2) % n
        counter += 1
    while stop > now():
        for _ in range(10_000):
            r = (r ** 2) % n
            # r = pow(r, 2, n)  # slower
            counter += 1
    print(counter)
    print("per sec:", counter / INTERVAL)
    # print("per hour", counter / INTERVAL * 3600)


def time_fixed_squarings(squarings):
    tlp = TLP(seed=SEED)
    pk, sk = tlp.setup(1, 1, keysize=KEYSIZE)
    n, _, r = pk
    start = now()
    for _ in range(squarings):
        r = (r ** 2) % n
    stop = now()
    seconds = (stop - start) / MILI_TO_S
    print(squarings / seconds)


if __name__ == '__main__':
    print(timer(count_squarings_in_fixed_time))
    # print(timer(time_fixed_squarings, 100_000_000))
