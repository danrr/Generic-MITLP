from gmpy2 import gmpy2

from lib import TLP
from lib.wrappers import SHA512Wrapper, Random

COMMITMENT_LENGTH = 128  # hard coded for hash commitments


class GMITLP:
    def __init__(self, *, tlp=TLP, hash_func=SHA512Wrapper, random=None, seed=None, **kwargs):
        if random is None:
            random = Random(seed=seed)
        self.random = random
        self.tlp = tlp(seed=seed, random=self.random, **kwargs)
        self.hash = hash_func

    def setup(self, intervals, squaring_per_second, keysize=2048):
        tlp_pk, tlp_sk = self.tlp.setup(1, 1, keysize)
        n, _, r_0 = tlp_pk
        _, _, phi_n, _ = tlp_sk

        # todo: can I reuse MITLP's setup?

        t = [gmpy2.mpz(interval * squaring_per_second) for interval in intervals]
        # todo: can I make this more efficient? fixed base
        a = [gmpy2.powmod(2, t_i, phi_n) for t_i in t]

        r = [r_0] + [self.random.gen_random_generator_mod_n(n) for _ in intervals[1:]]
        r_bin = [gmpy2.to_binary(ri) for ri in r]

        len_bytes = COMMITMENT_LENGTH // 8
        d = [self.random.gen_random_bytes(len_bytes) for _ in intervals]

        aux = (self.hash.name, len_bytes, [len(ri) for ri in r_bin])

        return (aux, n, t, r_0), (a, r_bin, d)

    def generate(self, m, pk, sk):
        # todo: generator function?
        aux, n, t, _ = pk
        a, r, d = sk
        z = len(m)
        if len(r) != z or len(d) != z:
            raise ValueError('length of m, r, and d must be equal')

        hash_list = [0] * z
        puzz_list = [(None, None)] * z
        for i in range(z):
            pk_i = n, t[i], gmpy2.from_binary(r[i])

            message = m[i] + d[i]
            hash_list[i] = self.hash.digest(message)

            if i != z - 1:
                message += r[i + 1]
            c_k, c_m = self.tlp.generate(pk_i, (None, None, None, a[i]), message)
            puzz_list[i] = (c_k, c_m)

        return puzz_list, hash_list

    def solve(self, pk, puzz):
        aux, n, t, r_i = pk
        _, len_d, len_r = aux
        z = len(puzz)

        for i in range(z):
            s_i = self.tlp.solve((n, t[i], r_i), puzz[i])

            if i < z - 1:
                len_r_i = len_r[i + 1]
                r_i = s_i[-len_r_i:]
                r_i = gmpy2.from_binary(r_i)
                message = s_i[:-len_r_i]
            else:
                message = s_i

            m_i = message[:-len_d]
            d_i = message[-len_d:]

            yield m_i, d_i

    def verify(self, m, d, h):
        assert h == self.hash.digest(m + d)
