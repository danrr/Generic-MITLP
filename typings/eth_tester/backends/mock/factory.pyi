from collections.abc import Generator

from _typeshed import Incomplete
from eth_tester.backends.common import merge_genesis_overrides as merge_genesis_overrides
from eth_tester.backends.mock.common import calculate_effective_gas_price as calculate_effective_gas_price
from eth_tester.constants import DYNAMIC_FEE_TRANSACTION_PARAMS as DYNAMIC_FEE_TRANSACTION_PARAMS
from eth_tester.utils.address import generate_contract_address as generate_contract_address
from eth_tester.utils.transactions import extract_transaction_type as extract_transaction_type

ZERO_32BYTES: Incomplete
ZERO_8BYTES: Incomplete
ZERO_ADDRESS: Incomplete
BLOCK_ELASTICITY_MULTIPLIER: int
BASE_FEE_MAX_CHANGE_DENOMINATOR: int

def bytes_repr(value) -> Generator[Incomplete, None, None]: ...
def fake_rlp_hash(value): ...
def add_hash(fn): ...
def create_transaction(transaction, block, transaction_index, is_pending, overrides: Incomplete | None = None): ...
def make_log(
    transaction, block, transaction_index, log_index, overrides: Incomplete | None = None
) -> Generator[Incomplete, None, None]: ...
def make_receipt(
    transaction, block, _transaction_index, overrides: Incomplete | None = None
) -> Generator[Incomplete, None, None]: ...

GENESIS_NONCE: bytes
BLANK_ROOT_HASH: bytes
EMPTY_UNCLE_HASH: bytes
POST_MERGE_DIFFICULTY: int
POST_MERGE_MIX_HASH: Incomplete
POST_MERGE_NONCE: bytes

def make_genesis_block(overrides: Incomplete | None = None): ...
def make_block_from_parent(parent_block, overrides: Incomplete | None = None) -> Generator[Incomplete, None, None]: ...
