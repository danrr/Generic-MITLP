from consts import KEYSIZE, MESSAGE, SEED, SQUARINGS_PER_SEC
from utils import add_times, get_size, timer, timer_with_output

from tlp_lib import DGMITLP, GMITLP, MITLP, TLP
from tlp_lib.protocols import (
    GMITLP_Encrypted_Message,
    GMITLP_Public,
    GMITLP_Secret,
    MITLP_Public,
    MITLP_Secret,
    Server_Info,
    TLP_Digest,
    TLP_Message,
    TLP_Public,
    TLP_Puzzle,
)

# todo: store in some format that can be output to csv
# todo: pyplot


def benchmark_time_tlp(messages: list[bytes], distinct_intervals: list[int], solve: bool):
    tlp = TLP(seed=SEED)

    puzzles: list[tuple[TLP_Public, TLP_Puzzle]] = []

    def tlp_setup_and_generate():
        puzzles.clear()
        seconds = 0
        for i, m in enumerate(messages):
            seconds += distinct_intervals[i]
            pk, sk = tlp.setup(seconds, SQUARINGS_PER_SEC[KEYSIZE], KEYSIZE)
            if solve:
                puzzles.append((pk, tlp.generate(pk, sk.a, m)))

    time = timer(tlp_setup_and_generate)
    print("TLP setup and generate", time)

    (n, _, _), (p, q, phi_n, _) = tlp.setup(1, SQUARINGS_PER_SEC[KEYSIZE], KEYSIZE)

    def gen_modulus(*, keysize: int):
        # keysize isn't used, as KEYSIZE constant affects instantiation above
        return n, p, q, phi_n

    def tlp_setup_and_generate_fixed_n():
        tlp = TLP(seed=SEED, gen_modulus=gen_modulus)
        seconds = 0
        for i, m in enumerate(messages):
            seconds += distinct_intervals[i]
            pk, sk = tlp.setup(seconds, SQUARINGS_PER_SEC[KEYSIZE], KEYSIZE)
            tlp.generate(pk, sk.a, m)

    time_fixed_n = timer(tlp_setup_and_generate_fixed_n)
    print("TLP setup and generate fixed n", time_fixed_n)

    if not solve:
        return

    def tlp_solve_sequentially():
        for pk, puzzle in puzzles:
            tlp.solve(pk, puzzle)

    time_solve = timer(tlp_solve_sequentially)
    print("TLP solve", time_solve)


def benchmark_time_mitlp(messages: list[bytes], instances: int, fixed_interval: int, solve: bool):
    mitlp = MITLP(seed=SEED)

    time_setup, (pk, sk) = timer_with_output(
        mitlp.setup, instances, fixed_interval, SQUARINGS_PER_SEC[KEYSIZE], KEYSIZE
    )
    print("MITLP setup", time_setup)

    time_generate, (puzz_list, hash_list) = timer_with_output(mitlp.generate, messages, pk, sk)
    print("MITLP generate", time_generate)

    if not solve:
        print("MITLP total", add_times(time_setup, time_generate))
        return

    sol: list[tuple[TLP_Message, TLP_Digest]] = []

    def mitlp_solve():
        sol.clear()
        for x in mitlp.solve(pk, puzz_list):
            sol.append(x)

    time_solve = timer(mitlp_solve)
    print("MITLP solve", time_solve)

    def mitlp_verify():
        for i, (m, d) in enumerate(sol):
            assert m == messages[i]
            mitlp.verify(m, d, hash_list[i])

    time_verify = timer(mitlp_verify)
    print("MITLP verify", time_verify)

    print("MITLP total", add_times(time_setup, time_generate, time_solve, time_verify))


def benchmark_time_gmitlp(messages: list[bytes], distinct_intervals: list[int], solve: bool):
    gmitlp = GMITLP(seed=SEED)

    time_setup, (pk, sk) = timer_with_output(gmitlp.setup, distinct_intervals, SQUARINGS_PER_SEC[KEYSIZE], KEYSIZE)
    print("GMITLP setup", time_setup)

    time_generate, (puzz_list, hash_list) = timer_with_output(gmitlp.generate, messages, pk, sk)
    print("GMITLP generate", time_generate)

    if not solve:
        print("GMITLP total", add_times(time_setup, time_generate))
        return

    sol: list[tuple[TLP_Message, TLP_Digest]] = []

    def gmitlp_solve():
        sol.clear()
        for x in gmitlp.solve(pk, puzz_list):
            sol.append(x)

    time_solve = timer(gmitlp_solve)
    print("GMITLP solve", time_solve)

    def gmitlp_verify():
        for i, (m, d) in enumerate(sol):
            assert m == messages[i]
            gmitlp.verify(m, d, hash_list[i])

    time_verify = timer(gmitlp_verify)
    print("GMITLP verify", time_verify)

    print("GMITLP total", add_times(time_setup, time_generate, time_solve, time_verify))


def benchmark_time_dgmitlp(messages: list[bytes], distinct_intervals: list[int], solve: bool):
    dgmitlp = DGMITLP(seed=SEED)

    time_client_setup, csk = timer_with_output(dgmitlp.client_setup)
    print("DGMITLP client setup", time_client_setup)

    time_client_delegation, (encrypted_messages, start_time) = timer_with_output(
        dgmitlp.client_delegation, messages, csk
    )
    print("DGMITLP client delegation", time_client_delegation)

    coins = [1] * len(distinct_intervals)
    server_info = Server_Info(1)
    time_server_delegation, (_, sc) = timer_with_output(
        dgmitlp.server_delegation, distinct_intervals, server_info, coins, start_time, 1, None, KEYSIZE
    )
    print("DGMITLP server delegation", time_server_delegation)

    time_helper_setup, (pk, sk) = timer_with_output(
        dgmitlp.helper_setup, distinct_intervals, SQUARINGS_PER_SEC[KEYSIZE], KEYSIZE
    )
    print("DGMITLP helper setup", time_helper_setup)

    time_helper_generate, puzz_list = timer_with_output(
        dgmitlp.helper_generate, encrypted_messages, pk, sk, start_time, sc
    )
    print("DGMITLP helper generate", time_helper_generate)

    if not solve:
        print(
            "DGMITLP total",
            add_times(
                time_client_setup,
                time_client_delegation,
                time_server_delegation,
                time_helper_setup,
                time_helper_generate,
            ),
        )
        return

    coins_acceptable = 1

    sol: list[tuple[GMITLP_Encrypted_Message, TLP_Digest]] = []

    def gdmitlp_solve():
        sol.clear()
        for x in dgmitlp.solve(sc, server_info, pk, puzz_list, coins_acceptable):
            sol.append(x)

    time_solve = timer(gdmitlp_solve)
    print("DGMITLP helper solve", time_solve)

    def dgmitlp_register():
        for m_, d in sol:
            dgmitlp.register(sc, m_, d)

    time_register = timer(dgmitlp_register)
    print("DGMITLP helper register", time_register)

    def dgmitlp_verify():
        for i in range(len(messages)):
            dgmitlp.verify(sc, i)

    time_verify, _ = timer_with_output(dgmitlp_verify)

    def dgmitlp_retrieve():
        for i, _ in enumerate(messages):
            dgmitlp.retrieve(sc, csk, i)

    time_retrieve = timer(dgmitlp_retrieve)
    print("DGMITLP retrieve", time_retrieve)

    print(
        "DGMITLP total",
        add_times(
            time_client_setup,
            time_client_delegation,
            time_server_delegation,
            time_helper_setup,
            time_helper_generate,
            time_solve,
            time_register,
            time_verify,
            time_retrieve,
        ),
    )


def get_size_of_output(
    output: tuple[MITLP_Public, MITLP_Secret] | tuple[GMITLP_Public, GMITLP_Secret]
) -> tuple[int, int, int, int, int, int, int, int, int]:
    (aux, n, t, r_0), (a, r, d) = output
    size_aux = get_size(aux)
    size_n = get_size(n)
    size_t = get_size(t)
    size_pk = size_n + size_t + get_size(r_0) + size_aux
    size_r = get_size(r)
    size_a = get_size(a)
    size_d = get_size(d)
    size_sk = size_r + size_a + size_d
    total_size = size_sk + size_pk
    return size_aux, size_n, size_t, size_r, size_a, size_d, size_pk, size_sk, total_size


def benchmark_size(instances: int, fixed_interval: int):
    headings = (
        "Size of aux",
        "Size of n",
        "Size of t",
        "Size of r",
        "Size of a",
        "Size of d",
        "Size of public key",
        "Size of secret key",
        "Total size",
    )

    mitlp = MITLP(seed=SEED)
    gmitlp = GMITLP(seed=SEED)

    distinct_intervals = [fixed_interval for _ in range(instances)]
    mitlp_size = get_size_of_output(mitlp.setup(instances, fixed_interval, SQUARINGS_PER_SEC[KEYSIZE], keysize=KEYSIZE))
    gmitlp_size = get_size_of_output(gmitlp.setup(distinct_intervals, SQUARINGS_PER_SEC[KEYSIZE], keysize=KEYSIZE))
    print(f"For {instances} instances of {fixed_interval} seconds each")
    print(f"{'TLP':20} {'MITLP': >20} {'GMITLP': >20} {'Difference': >20}")
    for heading, val1, val2 in zip(headings, mitlp_size, gmitlp_size):
        print(f"{heading:20} {val1: >20} {val2: >20} {val2 - val1: >20}")


def benchmark_time(instances: int, fixed_interval: int, solve: bool):
    distinct_intervals = [fixed_interval for _ in range(instances)]
    print(f"Setup time for {instances} instances of {fixed_interval} seconds each")
    messages = [MESSAGE] * instances
    benchmark_time_tlp(messages, distinct_intervals, solve)
    print()
    benchmark_time_mitlp(messages, instances, fixed_interval, solve)
    print()
    benchmark_time_gmitlp(messages, distinct_intervals, solve)
    print()
    benchmark_time_dgmitlp(messages, distinct_intervals, solve)
    print()


INSTANCES = [10**i for i in range(1, 3)]
FIXED_INTERVALS = [10**i for i in range(0, 9)]


def benchmark(solve: bool):
    fixed_interval = 1
    instances = 1000

    for instances in INSTANCES:
        benchmark_size(instances, fixed_interval)
        print()

    for instances in INSTANCES:
        benchmark_time(instances, fixed_interval, solve)

    for fixed_interval in FIXED_INTERVALS:
        benchmark_size(instances, fixed_interval)
        print()

    for fixed_interval in FIXED_INTERVALS:
        benchmark_time(instances, fixed_interval, solve)


if __name__ == "__main__":
    print("keysize:", KEYSIZE)
    benchmark(solve=True)
