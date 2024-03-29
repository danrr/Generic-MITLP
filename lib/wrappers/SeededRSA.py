from lib.wrappers.Random import Random


class SeededRSA:
    def __init__(self, *, seed=None):
        self.rand = Random(seed=seed)

    def gen_key(self, *, keysize=2048):
        p = self.rand.gen_random_prime(keysize // 2)
        q = self.rand.gen_random_prime(keysize // 2)
        n = p * q
        phi_n = (p - 1) * (q - 1)
        return n, p, q, phi_n
