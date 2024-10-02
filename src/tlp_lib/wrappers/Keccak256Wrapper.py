from typing import ClassVar

from cryptography.hazmat.primitives import hashes
from eth_utils import keccak


class Keccak256Wrapper:
    name: ClassVar[str] = "KECCAK256"

    @staticmethod
    def digest(message: bytes) -> bytes:
        return keccak(message)
