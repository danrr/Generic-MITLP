import math

from lib import TLP

from consts import SEED, SQUARINGS_PER_SEC, KEYSIZE, MESSAGE
from utils import timer


def benchmark_tlp_solve_single():
    time = 1
    tlp = TLP(seed=SEED)
    pk, sk = tlp.setup(time, SQUARINGS_PER_SEC[KEYSIZE], keysize=KEYSIZE)
    p = tlp.generate(pk, sk, MESSAGE)
    times = timer(tlp.solve, pk, p)

    print(times)
    for t in times:
        assert math.isclose(t, time, abs_tol=0.05)


if __name__ == "__main__":
    benchmark_tlp_solve_single()
