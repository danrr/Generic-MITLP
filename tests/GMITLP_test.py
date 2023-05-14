import pytest
from lib import GMITLP


@pytest.mark.parametrize("messages, seconds", [
    ([b""], [1]),
    ([b"test1"], [1]),
    ([b"test1", b"test2"], [1, 2]),
    ([b"test1", b"test2", b"test1", b"test2"], [1, 2, 1, 2]),
])
def test_mitlp_generic(messages, seconds):
    gmitlp = GMITLP()
    pk, sk = gmitlp.setup(seconds, 1)
    puzz_list, hash_list = gmitlp.generate(messages, pk, sk)
    s = gmitlp.solve(pk, puzz_list)
    for i, (m, d) in enumerate(s):
        assert m == messages[i]
        gmitlp.verify(m, d, hash_list[i])
