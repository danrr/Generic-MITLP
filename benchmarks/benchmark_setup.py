from collections import namedtuple

from lib import TLP, MITLP, GMITLP, DGMITLP
from utils import timer, get_size, add_times
from consts import SQUARINGS_PER_SEC, SEED, KEYSIZE, MESSAGE

# INSTANCES = [10 ** i for i in range(1, 7)]
INSTANCES = [10 ** i for i in range(1, 3)]


# todo: loop over different sizes of z
# todo: store in some format that can be output to csv
# todo: pyplot


def benchmark_time(instances, fixed_interval):
    distinct_intervals = [fixed_interval for _ in range(instances)]
    print(f"Setup time for {instances} instances of {fixed_interval} seconds each")
    messages = [MESSAGE] * instances
    benchmark_time_tlp(messages, distinct_intervals)
    print()
    benchmark_time_mitlp(messages, instances, fixed_interval)
    print()
    benchmark_time_gmitlp(messages, distinct_intervals)
    print()
    benchmark_time_dgmitlp(messages, distinct_intervals)
    print()


def benchmark_time_tlp(messages, distinct_intervals):
    tlp = TLP(seed=SEED)

    def tlp_setup_and_generate():
        seconds = 0
        for i, m in enumerate(messages):
            seconds += distinct_intervals[i]
            pk, sk = tlp.setup(seconds, SQUARINGS_PER_SEC[KEYSIZE], KEYSIZE)
            tlp.generate(pk, sk, m)

    time = timer(tlp_setup_and_generate)
    print("TLP setup and generate", time)

    (n, _, _), (p, q, phi_n, _) = tlp.setup(1, SQUARINGS_PER_SEC[KEYSIZE], KEYSIZE)

    def gen_modulus(keysize):
        # keysize isn't used, as KEYSIZE constant affects instantiation above
        return n, p, q, phi_n

    def tlp_setup_and_generate_fixed_n():
        tlp = TLP(seed=SEED, gen_modulus=gen_modulus)
        seconds = 0
        for i, m in enumerate(messages):
            seconds += distinct_intervals[i]
            pk, sk = tlp.setup(seconds, SQUARINGS_PER_SEC[KEYSIZE], KEYSIZE)
            tlp.generate(pk, sk, m)

    time_fixed_n = timer(tlp_setup_and_generate_fixed_n)
    print("TLP setup and generate fixed n", time_fixed_n)


def benchmark_time_mitlp(messages, instances, fixed_interval):
    mitlp = MITLP(seed=SEED)

    pk, sk = mitlp.setup(instances, fixed_interval, SQUARINGS_PER_SEC[KEYSIZE], KEYSIZE)
    time_setup = timer(mitlp.setup, instances, fixed_interval, SQUARINGS_PER_SEC[KEYSIZE], KEYSIZE)
    print("MITLP setup", time_setup)

    time_generate = timer(mitlp.generate, messages, pk, sk)
    print("MITLP generate", time_generate)

    print("MITLP total", add_times(time_setup, time_generate))


def benchmark_time_gmitlp(messages, distinct_intervals):
    gmitlp = GMITLP(seed=SEED)

    pk, sk = gmitlp.setup(distinct_intervals, SQUARINGS_PER_SEC[KEYSIZE], KEYSIZE)
    time_setup = timer(gmitlp.setup, distinct_intervals, SQUARINGS_PER_SEC[KEYSIZE], KEYSIZE)
    print("GMITLP setup", time_setup)

    time_generate = timer(gmitlp.generate, messages, pk, sk)
    print("GMITLP generate", time_generate)

    print("GMITLP total", add_times(time_setup, time_generate))


def benchmark_time_dgmitlp(messages, distinct_intervals):
    sc = namedtuple("mock_sc", ["commitments"], defaults=[[]])
    dgmitlp = DGMITLP(seed=SEED)

    csk = dgmitlp.client_setup()
    time_client_setup = timer(dgmitlp.client_setup)
    print("DGMITLP client setup", time_client_setup)

    encrypted_messages, start_time = dgmitlp.client_delegation(messages, csk)
    time_client_delegation = timer(dgmitlp.client_delegation, messages, csk)
    print("DGMITLP client delegation", time_client_delegation)

    pk, sk = dgmitlp.helper_setup(distinct_intervals, SQUARINGS_PER_SEC[KEYSIZE], KEYSIZE)
    time_helper_setup = timer(dgmitlp.helper_setup, distinct_intervals, SQUARINGS_PER_SEC[KEYSIZE], KEYSIZE)
    print("DGMITLP helper setup", time_helper_setup)

    time_helper_generate = timer(dgmitlp.helper_generate, encrypted_messages, pk, sk, start_time, sc)
    print("DGMITLP helper generate", time_helper_generate)

    print("DGMITLP total",
          add_times(time_client_setup, time_client_delegation, time_helper_setup, time_helper_generate))


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


def benchmark_size(instances, fixed_interval):
    headings = ('Size of n', 'Size of t', 'Size of r', 'Size of e', 'Size of d', 'Size of public key',
                'Size of secret key', 'Total size')

    mitlp = MITLP(seed=SEED)
    gmitlp = GMITLP(seed=SEED)

    distinct_intervals = [fixed_interval for _ in range(instances)]
    mitlp_size = get_size_of_output(
        mitlp.setup(instances, fixed_interval, SQUARINGS_PER_SEC[KEYSIZE], keysize=KEYSIZE))
    gmitlp_size = get_size_of_output(
        gmitlp.setup(distinct_intervals, SQUARINGS_PER_SEC[KEYSIZE], keysize=KEYSIZE))
    print(f"For {instances} instances of {fixed_interval} seconds each")
    print(f"{'TLP':20} {'MITLP': >20} {'GMITLP': >20} {'Difference': >20}")
    for heading, val1, val2 in zip(headings, mitlp_size, gmitlp_size):
        print(f"{heading:20} {val1: >20} {val2: >20} {val2 - val1: >20}")


def benchmark():
    fixed_interval = 10

    for instances in INSTANCES:
        benchmark_size(instances, fixed_interval)
        print()

    for instances in INSTANCES:
        benchmark_time(instances, fixed_interval)


if __name__ == "__main__":
    benchmark()
