from gmpy2 import gmpy2

from lib.wrappers import FernetWrapper, RsaWrapper, Random, SeededRSA


class TLP:
    def __init__(self, *, sym_enc=None, gen_modulus=None, seed=None, random=None):
        if sym_enc is None:
            sym_enc = FernetWrapper()
        self.sym_enc = sym_enc
        if gen_modulus is None:
            if seed is not None:
                gen_modulus = SeededRSA(seed=seed).gen_key
            else:
                gen_modulus = RsaWrapper.gen_key
        self.gen_modulus = gen_modulus
        if random is None:
            random = Random(seed=seed)
        self.gen_random_generator = random.gen_random_generator_mod_n

    def setup(self, interval, squarings_per_second, keysize=2048):
        n, p, q, phi_n = self.gen_modulus(keysize=keysize)
        r = self.gen_random_generator(n)
        t = gmpy2.mpz(interval) * squarings_per_second
        a = gmpy2.powmod(2, t, phi_n)
        return (n, t, r), (p, q, phi_n, a)

    def generate(self, pk, sk, message):
        n, t, r = pk
        _, _, _, a = sk

        k = self.sym_enc.generate_key()
        b = gmpy2.powmod(r, a, n)
        encrypted_message = self.sym_enc.encrypt(k, message)
        encrypted_key = int((k + b) % n)
        return encrypted_key, encrypted_message

    def solve(self, pk, puzzle):
        encrypted_key, encrypted_message = puzzle
        n, t, r = pk

        for i in range(t):
            r = r ** 2 % n
        key_int = int((encrypted_key - r) % n)
        message = self.sym_enc.decrypt(key_int, encrypted_message)
        return message
