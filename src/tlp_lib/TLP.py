from typing import Optional

from gmpy2 import mpz, powmod

from lib.protocols import TLP_Message, TLP_Public, TLP_Public_Input, TLP_Puzzle, TLP_Secret, TLP_Secret_Input
from lib.wrappers import FernetWrapper, Random, RsaWrapper, SeededRSA
from lib.wrappers.protocols import RandGenModN, RSAKeyGen, SymEnc


class TLP:
    def __init__(
        self,
        *,
        sym_enc: Optional[SymEnc] = None,
        gen_modulus: Optional[RSAKeyGen] = None,
        seed: Optional[int] = None,
        random: Optional[RandGenModN] = None,
    ):
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

    def setup(self, interval: int, squarings_per_second: int, keysize: int = 2048) -> tuple[TLP_Public, TLP_Secret]:
        n, p, q, phi_n = self.gen_modulus(keysize=keysize)
        r = self.gen_random_generator(n)
        t = mpz(interval) * squarings_per_second
        a = powmod(2, t, phi_n)
        return TLP_Public(n, t, r), TLP_Secret(p, q, phi_n, a)

    def generate(self, pk: TLP_Public_Input, sk: TLP_Secret_Input, message: TLP_Message) -> TLP_Puzzle:
        n, t, r = pk
        _, _, _, a = sk

        k = self.sym_enc.generate_key()
        b = powmod(r, a, n)
        encrypted_message = self.sym_enc.encrypt(k, message)
        encrypted_key = int((k + b) % n)
        return TLP_Puzzle(encrypted_key, encrypted_message)

    def solve(self, pk: TLP_Public_Input, puzzle: TLP_Puzzle) -> TLP_Message:
        encrypted_key, encrypted_message = puzzle
        n, t, r = pk

        for i in range(t):
            r = r**2 % n
        key_int = int((encrypted_key - r) % n)
        message = self.sym_enc.decrypt(key_int, encrypted_message)
        return message
