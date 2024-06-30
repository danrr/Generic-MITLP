from typing import Protocol


class HashFunc(Protocol):
    name: str

    def digest(self, message: bytes) -> bytes: ...


class SymEnc(Protocol):
    def generate_key(self) -> int: ...

    def encrypt(self, key_int: int, message: bytes) -> bytes: ...

    def decrypt(self, key_int: int, encrypted_message: bytes) -> bytes: ...


class RandGenModN(Protocol):
    def gen_random_generator_mod_n(self, n: int) -> int: ...


class RandGen(RandGenModN, Protocol):
    def gen_random_prime(self, bits: int) -> int: ...

    def gen_random_bytes(self, length: int) -> bytes: ...


class RSAKeyGen(Protocol):
    def __call__(self, *, keysize: int) -> tuple[int, int, int, int]: ...
