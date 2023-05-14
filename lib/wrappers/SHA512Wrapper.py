from cryptography.hazmat.primitives import hashes


class SHA512Wrapper:
    name = "SHA512"

    @staticmethod
    def digest(message):
        digest = hashes.Hash(hashes.SHA512())
        digest.update(message)
        return digest.finalize()
