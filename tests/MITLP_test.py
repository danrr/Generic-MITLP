from typing import Literal

import pytest

from tlp_lib import MITLP


@pytest.mark.parametrize("keysize", [1024, 2048])
@pytest.mark.parametrize(
    "messages",
    [
        [b""],
        [b"t"],
        [b"test"],
        [b"test1", b"test2"],
        [b"test1", b"test2", b"test2", b"test2", b"test2"],
    ],
)
def test_mitlp(keysize: Literal[1024, 2048], messages: list[bytes]):
    mitlp = MITLP()
    z = len(messages)
    pk, sk = mitlp.setup(z, 1, 1, keysize=keysize)
    puzz_list, hash_list = mitlp.generate(messages, pk, sk)
    s = mitlp.solve(pk, puzz_list)
    for i, (m, d) in enumerate(s):
        assert m == messages[i]
        mitlp.verify(m, d, hash_list[i])
