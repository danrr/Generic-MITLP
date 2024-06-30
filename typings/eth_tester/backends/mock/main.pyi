from collections.abc import Generator

from _typeshed import Incomplete
from eth_tester.backends.base import BaseChainBackend as BaseChainBackend
from eth_tester.exceptions import BlockNotFound as BlockNotFound
from eth_tester.exceptions import TransactionNotFound as TransactionNotFound
from eth_tester.utils.accounts import private_key_to_address as private_key_to_address
from eth_tester.utils.encoding import zpad as zpad

from ..pyevm.main import ZERO_ADDRESS as ZERO_ADDRESS
from .factory import create_transaction as create_transaction
from .factory import fake_rlp_hash as fake_rlp_hash
from .factory import make_block_from_parent as make_block_from_parent
from .factory import make_genesis_block as make_genesis_block
from .factory import make_receipt as make_receipt
from .serializers import serialize_block as serialize_block
from .serializers import serialize_full_transaction as serialize_full_transaction
from .serializers import serialize_receipt as serialize_receipt
from .serializers import serialize_transaction_as_hash as serialize_transaction_as_hash

def get_default_alloc(num_accounts: int = 10) -> Generator[Incomplete, None, None]: ...

class MockBackend(BaseChainBackend):
    alloc: Incomplete
    blocks: Incomplete
    block: Incomplete
    receipts: Incomplete
    fork_blocks: Incomplete
    genesis_alloc: Incomplete
    genesis_block: Incomplete
    def __init__(self, alloc: Incomplete | None = None, genesis_block: Incomplete | None = None) -> None: ...
    def take_snapshot(self): ...
    def revert_to_snapshot(self, snapshot) -> None: ...
    def reset_to_genesis(self) -> None: ...
    @property
    def account_state_lookup(self): ...
    def time_travel(self, timestamp) -> None: ...
    def mine_blocks(self, num_blocks: int = 1, coinbase=...) -> Generator[Incomplete, None, None]: ...
    def get_accounts(self): ...
    def add_account(self, private_key) -> None: ...
    def get_block_by_number(self, block_number, full_transactions: bool = False): ...
    def get_block_by_hash(self, block_hash, full_transactions: bool = False): ...
    def get_transaction_by_hash(self, transaction_hash): ...
    def get_transaction_receipt(self, transaction_hash): ...
    def get_nonce(self, account, block_number: Incomplete | None = None): ...
    def get_balance(self, account, block_number: Incomplete | None = None): ...
    def get_code(self, account, block_number: Incomplete | None = None): ...
    def send_raw_transaction(self, raw_transaction): ...
    def send_transaction(self, transaction): ...
    def send_signed_transaction(self, signed_transaction): ...
    def estimate_gas(self, transaction) -> None: ...
    def call(self, transaction, block_number: str = "latest") -> None: ...
    def get_fee_history(self, block_count: int = 1, newest_block: str = "latest", reward_percentiles=()): ...