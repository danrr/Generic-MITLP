from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa


class RsaWrapper:
    @staticmethod
    def gen_key(*, keysize=2048, seed=None):
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=keysize,
            backend=default_backend()
        )

        p, q = private_key.private_numbers().p, private_key.private_numbers().q
        n = private_key.public_key().public_numbers().n
        phi_n = (p - 1) * (q - 1)
        return n, p, q, phi_n
