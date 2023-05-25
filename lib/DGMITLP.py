from collections import namedtuple
from datetime import datetime
from itertools import accumulate
from operator import add

from lib import GMITLP
from lib.wrappers import Random, FernetWrapper

from lib.consts import SQUARINGS_PER_SEC_UPPER_BOUND


# Set fixed TOC = repeated squaring in Z_(p*q)
def custom_extra_delay(squarings_upper_bound, seconds, aux):
    squarings = aux.squarings
    assert squarings <= squarings_upper_bound
    return seconds * (squarings_upper_bound / squarings - 1)


class MockSC:
    def __init__(self, coins, start_time, extra_time, upper_bounds, helper_id):
        self.coins = coins
        self.start_time = start_time
        self.extra_time = extra_time
        self.upper_bounds = upper_bounds
        self.helper_id = helper_id
        self.commitments = []
        self.solutions = []
        self.initial_timestamp = datetime.now()

    def add_solution(self, solution, witness):
        time = datetime.now()
        self.solutions.append((solution, witness, time))
        return time

    def get_message_at(self, i):
        return self.solutions[i][0]


class DGMITLP:
    def __init__(self, *, sym_enc=None, gmitlp=GMITLP, random=None, seed=None, SC=MockSC, **kwargs):
        if random is None:
            random = Random(seed=seed)
        self.random = random
        if sym_enc is None:
            sym_enc = FernetWrapper()
        self.sym_enc = sym_enc
        self.gmitlp = gmitlp(seed=seed, random=self.random, sym_enc=self.sym_enc, **kwargs)
        self.SC = SC

    def client_setup(self):
        return self.sym_enc.generate_key()

    def client_delegation(self, messages, csk):
        start_time = 0  # todo: allow for delays
        return [self.sym_enc.encrypt(csk, message) for message in messages], start_time
        # todo: send encrypted messages to TPH and start_time to TPH and S

    def server_delegation(self, intervals, server_info, coins, start_time, helper_id, squarings_upper_bound=None,
                          keysize=2048,
                          cdeg=custom_extra_delay):
        if squarings_upper_bound is None:
            squarings_upper_bound = SQUARINGS_PER_SEC_UPPER_BOUND[keysize]

        extra_time = [cdeg(squarings_upper_bound, interval, server_info) for interval in intervals]
        # todo: integrate with an actual smart contract
        upper_bounds = list(
            accumulate(
                [start_time] +
                list(
                    map(add, intervals, extra_time)
                )
            )
        )[1:]
        sc = self.SC(coins=coins, start_time=start_time, extra_time=extra_time, upper_bounds=upper_bounds,
                     helper_id=helper_id)
        return extra_time, sc

    def helper_setup(self, intervals, squaring_per_second, keysize=2048):
        return self.gmitlp.setup(intervals, squaring_per_second, keysize=keysize)

    def helper_generate(self, messages, pk, sk, start_time, sc):
        puzz_list, hash_list = self.gmitlp.generate(messages, pk, sk)
        sc.commitments = hash_list
        return puzz_list
        # todo: use start_time to send puzz_list to TPH

    def solve(self, sc, server_info, pk, puzz, coins_acceptable):
        coins = sc.coins
        if coins < coins_acceptable:
            return None, False

        _, _, t, _ = pk
        upper_bounds = sc.upper_bounds
        squarings_per_sec = server_info.squarings

        prev_bound = 0
        for i, upper_bound in enumerate(upper_bounds):
            server_time = t[i] / squarings_per_sec
            maximum_time = upper_bound - prev_bound

            if server_time > maximum_time:
                return None, False
            prev_bound = upper_bound

        return self.gmitlp.solve(pk, puzz)

    def register(self, sc, solution, commitment):
        return sc.add_solution(solution, commitment)

    def verify(self, sc, i):
        solution, witness, time_solved = sc.solutions[i]
        commitment = sc.commitments[i]
        time_to_solve = (time_solved - sc.initial_timestamp).total_seconds()
        upper_bound = sc.upper_bounds[i]
        assert time_to_solve < upper_bound
        self.gmitlp.verify(solution, witness, commitment)

    def pay(self, sc, i, z):
        coins = sc.coins // z
        try:
            self.verify(sc, i)
            print(f"paying TPH' {coins}")
        except AssertionError:
            print(f"paying S back {coins}")

    def retrieve(self, sc, csk, i):
        encrypted_message = sc.get_message_at(i)
        return self.sym_enc.decrypt(csk, encrypted_message)
