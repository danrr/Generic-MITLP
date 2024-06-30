import pytest

from tlp_lib import GMITLP


@pytest.mark.parametrize("keysize", [1024, 2048])
@pytest.mark.parametrize(
    "messages, intervals",
    [
        ([b""], [1]),
        ([b"test1"], [1]),
        ([b"test1", b"test2"], [1, 2]),
        ([b"test1", b"test2", b"test1", b"test2"], [1, 2, 1, 2]),
    ],
)
def test_gmitlp(keysize, messages, intervals):
    gmitlp = GMITLP()
    pk, sk = gmitlp.setup(intervals, 1, keysize=keysize)
    puzz_list, hash_list = gmitlp.generate(messages, pk, sk)
    s = gmitlp.solve(pk, puzz_list)
    for i, (m, d) in enumerate(s):
        assert m == messages[i]
        gmitlp.verify(m, d, hash_list[i])
