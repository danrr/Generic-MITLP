import pytest
from lib import DGMITLP


@pytest.mark.parametrize("messages, seconds", [
    ([b""], [1]),
    ([b"test1"], [1]),
    ([b"test1", b"test2"], [1, 2]),
    ([b"test1", b"test2", b"test1", b"test2"], [1, 2, 1, 2]),
])
def test_mitlp_generic(messages, seconds):
    dgmitlp = DGMITLP()
    csk = dgmitlp.client_setup()
    encrypted_messages = dgmitlp.client_delegation(messages, csk)
    pk, sk = dgmitlp.helper_setup(seconds, 1)
    puzz_list, hash_list = dgmitlp.helper_generate(encrypted_messages, pk, sk)

    upper_bounds = []
    server_info = {}
    coins = []
    coins_ = 0

    s = dgmitlp.solve(upper_bounds, server_info, pk, puzz_list, coins, coins_)
    for i, (m_, d) in enumerate(s):
        m = dgmitlp.retrieve(csk, m_)
        assert m == messages[i]
        dgmitlp.register(m_, d, hash_list[i])
