from collections.abc import Generator

from _typeshed import Incomplete
from eth_tester.backends.base import BaseChainBackend as BaseChainBackend
from eth_tester.backends.common import merge_genesis_overrides as merge_genesis_overrides
from eth_tester.constants import BLOB_TX_TYPE as BLOB_TX_TYPE
from eth_tester.constants import DYNAMIC_FEE_TRANSACTION_PARAMS as DYNAMIC_FEE_TRANSACTION_PARAMS
from eth_tester.exceptions import BackendDistributionNotFound as BackendDistributionNotFound
from eth_tester.exceptions import BlockNotFound as BlockNotFound
from eth_tester.exceptions import TransactionFailed as TransactionFailed
from eth_tester.exceptions import TransactionNotFound as TransactionNotFound
from eth_tester.exceptions import ValidationError as ValidationError
from eth_typing import Address as Address

from ...validation.inbound import validate_inbound_withdrawals as validate_inbound_withdrawals
from .serializers import serialize_block as serialize_block
from .serializers import serialize_transaction as serialize_transaction
from .serializers import serialize_transaction_receipt as serialize_transaction_receipt
from .utils import is_supported_pyevm_version_available as is_supported_pyevm_version_available

ZERO_ADDRESS: Incomplete
ZERO_HASH32: Incomplete
EIP838_SIG: bytes
EMPTY_RLP_LIST_HASH: bytes
BLANK_ROOT_HASH: bytes
GENESIS_BLOCK_NUMBER: int
GENESIS_DIFFICULTY: int
GENESIS_GAS_LIMIT: int
GENESIS_COINBASE = ZERO_ADDRESS
GENESIS_NONCE: bytes
GENESIS_MIX_HASH = ZERO_HASH32
GENESIS_EXTRA_DATA: bytes
GENESIS_INITIAL_ALLOC: Incomplete
MINIMUM_GAS_ESTIMATE: int
GAS_ESTIMATE_BUFFER: float

def get_default_account_state(overrides: Incomplete | None = None): ...
def get_default_account_keys(quantity: Incomplete | None = None) -> Generator[Incomplete, None, None]: ...
def get_account_keys_from_mnemonic(
    mnemonic, quantity: Incomplete | None = None, hd_path: Incomplete | None = None
) -> Generator[Incomplete, None, None]: ...
def generate_genesis_state_for_keys(
    account_keys, overrides: Incomplete | None = None
) -> Generator[Incomplete, None, None]: ...
def get_default_genesis_params(overrides: Incomplete | None = None): ...
def setup_tester_chain(
    genesis_params: Incomplete | None = None,
    genesis_state: Incomplete | None = None,
    num_accounts: Incomplete | None = None,
    vm_configuration: Incomplete | None = None,
    mnemonic: Incomplete | None = None,
    hd_path: Incomplete | None = None,
    genesis_is_post_merge: bool = True,
): ...

class PyEVMBackend(BaseChainBackend):
    chain: Incomplete
    account_keys: Incomplete
    def __init__(
        self,
        genesis_parameters: Incomplete | None = None,
        genesis_state: Incomplete | None = None,
        vm_configuration: Incomplete | None = None,
        mnemonic: Incomplete | None = None,
        hd_path: Incomplete | None = None,
    ) -> None: ...
    @classmethod
    def from_mnemonic(
        cls,
        mnemonic: str,
        genesis_state_overrides: Incomplete | None = None,
        num_accounts: Incomplete | None = None,
        genesis_parameters: Incomplete | None = None,
        vm_configuration: Incomplete | None = None,
        hd_path: Incomplete | None = None,
    ) -> PyEVMBackend: ...
    @classmethod
    def generate_genesis_params(cls, overrides: Incomplete | None = None): ...
    @classmethod
    def generate_genesis_state(
        cls,
        overrides: Incomplete | None = None,
        num_accounts: Incomplete | None = None,
        mnemonic: Incomplete | None = None,
        hd_path: Incomplete | None = None,
    ): ...
    def reset_to_genesis(
        self,
        genesis_params: Incomplete | None = None,
        genesis_state: Incomplete | None = None,
        num_accounts: Incomplete | None = None,
        vm_configuration: Incomplete | None = None,
        mnemonic: Incomplete | None = None,
        hd_path: Incomplete | None = None,
    ) -> None: ...
    def take_snapshot(self): ...
    def revert_to_snapshot(self, snapshot) -> None: ...
    def time_travel(self, to_timestamp): ...
    def mine_blocks(self, num_blocks: int = 1, coinbase=...) -> Generator[Incomplete, None, None]: ...
    def get_accounts(self) -> Generator[Incomplete, None, None]: ...
    def add_account(self, private_key) -> None: ...
    def get_block_by_number(self, block_number, full_transaction: bool = True): ...
    def get_block_by_hash(self, block_hash, full_transaction: bool = True): ...
    def get_transaction_by_hash(self, transaction_hash): ...
    def get_transaction_receipt(self, transaction_hash): ...
    def get_fee_history(
        self, block_count: int = 1, newest_block: str = "latest", reward_percentiles: list[int] = ()
    ): ...
    def get_nonce(self, account, block_number: str = "latest"): ...
    def get_balance(self, account, block_number: str = "latest"): ...
    def get_code(self, account, block_number: str = "latest"): ...
    def get_storage(self, account: Address, slot: int, block_number: str = "latest") -> bytes: ...
    def get_base_fee(self, block_number: str = "latest"): ...
    def send_raw_transaction(self, raw_transaction): ...
    def send_signed_transaction(self, signed_transaction, block_number: str = "latest"): ...
    def send_transaction(self, transaction): ...
    def apply_withdrawals(self, withdrawals_list: list[dict[str, int | str]]) -> None: ...
    def estimate_gas(self, transaction, block_number: str = "latest"): ...
    def is_eip838_error(self, error): ...
    def call(self, transaction, block_number: str = "latest"): ...
