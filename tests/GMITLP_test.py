import pytest

from implementation import GMITLP
@pytest.mark.parametrize("messages, seconds", [
    (["test1", "test2"], [1, 2]),
    (["test1", b"test2"], [1, 2]),
])
def test_mitlp_generic(messages, seconds):
    pk, sk = GMITLP.setup(seconds, 1)
    _, puzz_list, hash_list = GMITLP.generate(messages, pk, sk)
    s = GMITLP.solve(pk, puzz_list)
    for i, (m, d) in enumerate(s):
        assert m == bytes(messages[i], 'utf-8')
        GMITLP.verify(m, d, hash_list[i])
