from typing import NamedTuple, Optional
from collections.abc import Sequence

from gmpy2 import gmpy2

from lib import TLP
from lib.protocols import TLP_Message, TLP_type, TLPInterface
from lib.wrappers import Random, SHA512Wrapper
from lib.wrappers.protocols import HashFunc, RandGen

COMMITMENT_LENGTH = 128  # hard coded for hash commitments

MITLP_Auxiliary_Info = NamedTuple("MITLP_Auxiliary_Info", [("hash_name", str), ("len_commitment", int), ("len_r", int)])


class MITLP:
    def __init__(
        self,
        *,
        tlp: TLP_type = TLP,
        hash_func: HashFunc = SHA512Wrapper,
        random: Optional[RandGen] = None,
        seed: Optional[int] = None,
        **kwargs,
    ):
        if random is None:
            random = Random(seed=seed)
        self.random = random
        self.tlp = tlp(seed=seed, random=self.random, **kwargs)
        self.hash = hash_func

    def setup(self, z: int, interval: int, squaring_per_second: int, keysize: int = 2048):
        if z < 1:
            raise ValueError("z must be greater than 0")

        tlp_pk, tlp_sk = self.tlp.setup(interval, squaring_per_second, keysize)
        n, t, r_0 = tlp_pk
        _, _, _, a = tlp_sk

        r = [r_0] + [self.random.gen_random_generator_mod_n(n) for _ in range(z - 1)]
        len_r = keysize // 8
        r_bin = [ri.to_bytes(length=len_r) for ri in r]
        len_commitment = COMMITMENT_LENGTH // 8
        d = [self.random.gen_random_bytes(len_commitment) for _ in range(z)]

        aux = MITLP_Auxiliary_Info(self.hash.name, len_commitment, len_r)

        return (aux, n, t, r_0), (a, r_bin, d)

    def generate(self, m: Sequence[TLP_Message], pk, sk):
        # todo: generator function?
        aux, n, t, _ = pk
        a, r, d = sk
        z = len(m)
        if len(r) != z or len(d) != z:
            raise ValueError("length of m, r, and d must be equal")

        hash_list = [(0, b"")] * z
        puzz_list = [(None, None)] * z
        for i in range(z):
            pk_i = n, t, gmpy2.mpz.from_bytes(r[i])

            message = m[i] + d[i]
            hash_list[i] = self.hash.digest(message)

            if i != z - 1:
                message += r[i + 1]
            c_k, c_m = self.tlp.generate(pk_i, (None, None, None, a), message)
            puzz_list[i] = (c_k, c_m)

        return puzz_list, hash_list

    def solve(self, pk, puzz):
        aux, n, t, r_i = pk
        _, len_d, len_r = aux
        z = len(puzz)

        for i in range(z):
            s_i = self.tlp.solve((n, t, r_i), puzz[i])

            if i < z - 1:
                r_i = s_i[-len_r:]
                r_i = gmpy2.mpz.from_bytes(r_i)
                message = s_i[:-len_r]
            else:
                message = s_i

            m_i = message[:-len_d]
            d_i = message[-len_d:]

            yield m_i, d_i

    def verify(self, m, d, h):
        assert h == self.hash.digest(m + d)
