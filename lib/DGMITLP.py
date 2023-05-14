from lib import GMITLP
from lib.wrappers import Random, FernetWrapper

class DGMITLP:
    def __init__(self, *, sym_enc=None, gmitlp=GMITLP, random=None, seed=None, **kwargs):
        if random is None:
            random = Random(seed=seed)
        self.random = random
        if sym_enc is None:
            sym_enc = FernetWrapper()
        self.sym_enc = sym_enc
        self.gmitlp = gmitlp(seed=seed, random=self.random, sym_enc=self.sym_enc, **kwargs)

    def client_setup(self):
        return self.sym_enc.generate_key()

    def client_delegation(self, messages, csk):
        return [self.sym_enc.encrypt(csk, message) for message in messages]

    def server_delegation(self):
        # todo: implement
        # todo: CEDG(ToC, S, ̄∆j, aux) → Ψ
        pass

    def helper_setup(self, seconds, squaring_per_second, keysize=2048):
        return self.gmitlp.setup(seconds, squaring_per_second, keysize=keysize)

    def helper_generate(self, messages, pk, sk):
        return self.gmitlp.generate(messages, pk, sk)
        # todo: send puzz_list to TPH, hash_list to smart contract

    def solve(self, upper_bounds, server_info, pk, puzz, coins, coins_):
        # todo: check coins vs coins_
        # todo: check elements of phi (upper_bounds) against server_info
        return self.gmitlp.solve(pk, puzz)
        pass

    def prove(self):
        # todo: this might not be needed
        pass

    def register(self, m, d, h):
        # todo: check it's on time
        self.gmitlp.verify(m, d, h)
        pass

    def pay(self):
        # todo: interact with smart contract
        pass

    def retrieve(self, csk, encrypted_message):
        # todo: interact with smart contract
        return self.sym_enc.decrypt(csk, encrypted_message)
