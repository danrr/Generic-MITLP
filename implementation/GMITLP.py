import os
from gmpy2 import gmpy2
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa

from implementation.wrappers import SHA512Wrapper, FernetWrapper


def setup(seconds, squarings_per_second, keysize=2048):
    z = len(seconds)

    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=keysize,
        backend=default_backend()
    )

    p, q = private_key.private_numbers().p, private_key.private_numbers().q
    n = private_key.public_key().public_numbers().n
    phi_n = (p - 1) * (q - 1)

    t = [0]*z
    for i in range(z):
        t[i] = gmpy2.mpz(seconds[i] * squarings_per_second)

    e = gmpy2.powmod_exp_list(2, t, phi_n)

    r = [0] * z

    for i in range(0, z):
        # generate lists of generators
        r[i] = int.from_bytes(os.urandom(128), 'big') % n

    d = [0] * z
    for i in range(z):
        # generate lists of random commitment
        d[i] = os.urandom(128)

    pk = (n, t, r[0])
    sk = e, r, d
    return pk, sk


def generate(m, pk, sk):
    n, t, _ = pk
    e, r, d = sk
    z = len(m)
    if len(r) != z or len(d) != z:
        raise ValueError('length of m, r, and d must be equal')

    hash_list = [0] * z
    puzz_list = [0] * z
    for i in range(z - 1, -1, -1):
        if type(m[i]) != 'bytes':
            if type(m[i]) != 'string':
                m[i] = str(m[i])
            m_byte = bytes(m[i], 'utf-8')
        else:
            m_byte = m[i]

        message = m_byte + d[i]

        if i != z - 1:
            r_byte = r[i + 1].to_bytes(128, 'big')
            message += r_byte

        b = pow(r[i], e[i], n)

        key_int = FernetWrapper.generate_key()
        c_m = FernetWrapper.encrypt(key_int, message)

        c_k = (key_int + b) % n

        puzz_list[i] = (c_k, c_m)
        hash_list[i] = SHA512Wrapper.hash(m_byte + d[i])

    return pk, puzz_list, hash_list


def solve(pk, puzz):
    n, t, r_i = pk
    z = len(puzz)

    s = [0] * z
    for i in range(z):
        c_k, c_m = puzz[i]

        for _ in range(t[i]):
            r_i = pow(r_i, 2, n)
        key_int = (c_k - r_i) % n
        x_i = FernetWrapper.decrypt(int(key_int), c_m)

        if i < z - 1:
            message = x_i[:-128]
            r_i = int.from_bytes(x_i[-128:], 'big')
        else:
            message = x_i

        m_i = message[:-128]
        d_i = message[-128:]

        s[i] = (m_i, d_i)
        yield s[i]


def verify(m, d, h):
    h_prime = SHA512Wrapper.hash(m + d)
    assert h == h_prime
