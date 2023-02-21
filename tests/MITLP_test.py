import pytest

from implementation import MITLP


@pytest.mark.parametrize("messages", [
    ["test"],
    [12],
    ["test1", "test2"],
    ["test1", b"test2"],
])
def test_mitlp(messages):
    z = len(messages)
    pk, sk = MITLP.setup(z, 1, 1)
    _, puzz_list, hash_list = MITLP.generate(messages, pk, sk)
    s = MITLP.solve(pk, puzz_list)
    for i, (m, d) in enumerate(s):
        assert m == bytes(messages[i], 'utf-8')
        MITLP.verify(m, d, hash_list[i])

