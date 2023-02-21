from cryptography.hazmat.primitives import hashes


class SHA512Wrapper:
    @staticmethod
    def hash(message):
        digest = hashes.Hash(hashes.SHA512())
        digest.update(message)
        return digest.finalize()
