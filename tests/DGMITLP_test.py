from pathlib import Path
from unittest.mock import Mock

import math
from collections import namedtuple

import pytest
from lib import DGMITLP, custom_extra_delay
from lib.consts import SQUARINGS_PER_SEC_UPPER_BOUND
from lib.smartcontracts import MockSC, EthereumSC

Server_info = namedtuple("Aux_server_info", ["squarings"])


@pytest.mark.parametrize("keysize", [
    1024,
    2048
])
def test_cdeg(keysize):
    minimum_delay = 10

    assert math.isclose(0, custom_extra_delay(SQUARINGS_PER_SEC_UPPER_BOUND[keysize], minimum_delay,
                                              Server_info(squarings=SQUARINGS_PER_SEC_UPPER_BOUND[keysize])))
    assert math.isclose(minimum_delay, custom_extra_delay(SQUARINGS_PER_SEC_UPPER_BOUND[keysize], minimum_delay,
                                                          Server_info(
                                                              squarings=SQUARINGS_PER_SEC_UPPER_BOUND[keysize] // 2)))


def test_dgmitlp_too_few_coins():
    coins = [0]
    coins_acceptable = 1
    sc = namedtuple("mock_sc", ["coins"])(coins)
    dgmitlp = DGMITLP()
    assert (None, False) == dgmitlp.solve(sc, {}, (), [], coins_acceptable)


@pytest.mark.parametrize("keysize", [
    1024,
    2048
])
def test_dgmitlp_helper_too_slow(keysize):
    coins = [1, 1]
    coins_acceptable = 1
    intervals = [1, 2]
    start_time = 0
    helper_id = 1
    best_helper = Server_info(squarings=SQUARINGS_PER_SEC_UPPER_BOUND[keysize])
    weaker_helper = Server_info(squarings=SQUARINGS_PER_SEC_UPPER_BOUND[keysize] - 1)

    dgmitlp = DGMITLP()
    pk, _ = dgmitlp.helper_setup(intervals, SQUARINGS_PER_SEC_UPPER_BOUND[keysize])
    _, sc = dgmitlp.server_delegation(intervals, best_helper, coins, start_time, helper_id, keysize=keysize)
    dgmitlp.gmitlp = Mock(solve=Mock())
    assert (None, False) == dgmitlp.solve(sc, weaker_helper, pk, [], coins_acceptable)
    assert dgmitlp.gmitlp.solve.call_count == 0


@pytest.mark.parametrize("keysize", [
    1024,
    2048
])
def test_dgmitlp_helper_good_enougjh(keysize):
    coins = [1, 1]
    coins_acceptable = 1
    intervals = [1, 2]
    start_time = 0
    helper_id = 1
    best_helper = Server_info(squarings=SQUARINGS_PER_SEC_UPPER_BOUND[keysize])
    weaker_helper = Server_info(squarings=SQUARINGS_PER_SEC_UPPER_BOUND[keysize] - 1)

    dgmitlp = DGMITLP()
    pk, _ = dgmitlp.helper_setup(intervals, SQUARINGS_PER_SEC_UPPER_BOUND[keysize])
    _, sc = dgmitlp.server_delegation(intervals, weaker_helper, coins, start_time, helper_id, keysize=keysize)
    dgmitlp.gmitlp = Mock(solve=Mock(return_value="solved_puzzles"))
    assert "solved_puzzles" == dgmitlp.solve(sc, best_helper, pk, [], coins_acceptable)
    assert dgmitlp.gmitlp.solve.call_count == 1


@pytest.mark.parametrize("keysize", [
    1024,
    2048
])
@pytest.mark.parametrize("messages, intervals", [
    ([b""], [1]),
    ([b"test1"], [1]),
    ([b"test1", b"test2"], [1, 2]),
    ([b"test1", b"test2", b"test1", b"test2"], [1, 2, 1, 2]),
])
@pytest.mark.parametrize("sc", [
    MockSC(),
    EthereumSC(contract_path=str(Path("contracts/SmartContract.sol").resolve()))
])
def test_dgmitlp(keysize, messages, intervals, sc):
    squarigns_per_second_helper = 1

    coins = [1] * len(intervals)
    coins_acceptable = 1

    client_helper_id = 1
    server_id = 0
    server_helper_id = 2
    server_info = Server_info(squarings=1)

    helper_id = client_helper_id

    dgmitlp = DGMITLP(SC=sc)

    # client
    csk = dgmitlp.client_setup()
    encrypted_messages, start_time = dgmitlp.client_delegation(messages, csk)

    # server
    if type(sc) is EthereumSC:
        # Generate an address for the client helper and save it
        sc.switch_to_account(client_helper_id)
        helper_id = sc.account
    sc.switch_to_account(server_id)

    extra_time, sc = dgmitlp.server_delegation(intervals, server_info, coins, start_time, helper_id,
                                               squarings_upper_bound=SQUARINGS_PER_SEC_UPPER_BOUND[keysize],
                                               keysize=keysize)

    # TPH
    sc.switch_to_account(client_helper_id)
    pk, sk = dgmitlp.helper_setup(intervals, squarigns_per_second_helper)
    puzz_list = dgmitlp.helper_generate(encrypted_messages, pk, sk, start_time, sc)

    # TPH'
    sc.switch_to_account(server_helper_id)
    s = dgmitlp.solve(sc, server_info, pk, puzz_list, coins_acceptable)
    for (m_, d) in s:
        dgmitlp.register(sc, m_, d)

    # server
    sc.switch_to_account(server_id)
    for i, message in enumerate(messages):
        dgmitlp.pay(sc, i)
        m = dgmitlp.retrieve(sc, csk, i)
        assert m == message
