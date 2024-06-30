from typing import ClassVar

from cryptography.hazmat.primitives import hashes


class SHA512Wrapper:
    name: ClassVar[str] = "SHA512"

    @staticmethod
    def digest(message: bytes) -> bytes:
        digest = hashes.Hash(hashes.SHA512())
        digest.update(message)
        return digest.finalize()
