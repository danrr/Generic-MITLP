import pytest

from lib.wrappers import SeededRSA

from lib import TLP


@pytest.mark.parametrize("message", [
    b"",
    b"t",
    b"test2",
    b"test2test2test2test2test2",
])
@pytest.mark.parametrize("seed", [
    None,
    1234,
])
def test_tlp(message, seed):
    tlp = TLP(seed=seed)

    pk, sk = tlp.setup(1, 1)
    p = tlp.generate(pk, sk, message)
    m = tlp.solve(pk, p)
    if seed is not None:
        assert pk[0] == SeededRSA(seed=seed).gen_key()[0]
    assert m == message

