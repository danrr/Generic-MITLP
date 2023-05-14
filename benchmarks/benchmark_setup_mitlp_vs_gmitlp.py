import functools
import math
import sys
import timeit

from gmpy2 import gmpy2

from lib import MITLP, GMITLP

REPEAT = 1
SQUARINGS = 100_000
SEED=1234

instances = 100000
fixed_interval = 1_000_000

# random_state = gmpy2.random_state()
# b = math.ceil(math.log2(fixed_interval)) + 1
# distinct_intervals = [gmpy2.mpz_urandomb(random_state, b) for _ in range(instances)]
distinct_intervals = [fixed_interval for _ in range(instances)]


def timer(f, *args):
    return timeit.Timer(functools.partial(f, *args)).repeat(
        repeat=int(REPEAT),
        number=int(1))


def get_size(x):
    size = sys.getsizeof(x)
    if hasattr(x, '__iter__') and not isinstance(x, (str, bytes, bytearray)):
        for y in x:
            size += get_size(y)
    return size


def benchmark_time():
    mitlp = MITLP(seed=SEED)
    gmitlp = GMITLP(seed=SEED)
    [t1] = timer(mitlp.setup, instances, fixed_interval, SQUARINGS)
    [t2] = timer(gmitlp.setup, distinct_intervals, SQUARINGS)
    print(f"Setup time for {instances} instances of {fixed_interval} seconds each")
    print("MITLP", t1)
    print("GMITLP", t2)


def get_size_of_output(output):
    (aux, n, t, r_0), (e, r, d) = output
    size_n = get_size(n)
    size_t = get_size(t)
    size_pk = get_size(n) + get_size(t) + get_size(r[0])
    size_r = get_size(r)
    size_e = get_size(e)
    size_d = get_size(d)
    size_sk = size_r + size_e + size_d
    total_size = size_n + size_t + size_r + size_e + size_d
    return size_n, size_t, size_r, size_e, size_d, size_pk, size_sk, total_size


def benchmark_size():
    headings = ('Size of m', 'Size of t', 'Size of r', 'Size of e', 'Size of d', 'Size of public key',
                'Size of secret key', 'Total size')

    mitlp = MITLP(seed=SEED)
    gmitlp = GMITLP(seed=SEED)
    mitlp = get_size_of_output(mitlp.setup(instances, fixed_interval, SQUARINGS))
    gmitlp = get_size_of_output(gmitlp.setup(distinct_intervals, SQUARINGS))
    print(f"For {instances} instances of {fixed_interval} seconds each")
    print(f"{'TLP':20} {'MITLP': >20} {'GMITLP': >20} {'Difference': >20}")
    for heading, val1, val2 in zip(headings, mitlp, gmitlp):
        print(f"{heading:20} {val1: >20} {val2: >20} {val2 - val1: >20}")


#     sizes: n - RSA modulus - 2048 bits - 300 bytes
#            t - list of intervals - z * 48 bytes + list overhead vs 48 bytes
#            r - list of random bases - z * 164 bytes + list overhead
#            e - list of exponents - z * 296 bytes + list overhead vs 296 bytes
#            d - list of commitments - z * 164 bytes + list overhead

if __name__ == "__main__":
    benchmark_size()
    print()
    benchmark_time()
