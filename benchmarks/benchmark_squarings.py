import time

from gmpy2 import gmpy2

from lib.wrappers import SeededRSA, Random

KEYSIZE = 1024
INTERVAL = 300
SEED = 1234


def main():
    n, p, q, phi_n = SeededRSA(seed=1234).gen_key(keysize=KEYSIZE)
    random = Random(seed=1234)
    r = random.gen_random_generator_mod_n(n)
    r = gmpy2.mpz(r)
    counter = 0
    start = time.process_time()
    while start + INTERVAL > time.process_time():
        r = pow(r, 2, n)
        counter += 1
    print(counter)
    print(counter / INTERVAL)
    print(counter / INTERVAL * 3600)


if __name__ == '__main__':
    main()
