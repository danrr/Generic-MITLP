from _typeshed import Incomplete
from eth_tester.constants import BLOB_TRANSACTION_PARAMS as BLOB_TRANSACTION_PARAMS
from eth_tester.constants import BLOCK_NUMBER_META_VALUES as BLOCK_NUMBER_META_VALUES
from eth_tester.exceptions import ValidationError as ValidationError
from eth_typing import HexStr as HexStr

from .common import validate_address as validate_address
from .common import validate_dict as validate_dict
from .common import validate_positive_integer as validate_positive_integer
from .common import validate_text as validate_text
from .common import validate_transaction_type as validate_transaction_type
from .common import validate_uint8 as validate_uint8
from .common import validate_uint64 as validate_uint64
from .common import validate_uint256 as validate_uint256

def is_32_bytes(value): ...
def is_32byte_hex_string(value): ...
def is_topic(value): ...
def validate_32_byte_hex_value(value, name) -> None: ...

MAX_TIMESTAMP: int

def validate_timestamp(value) -> None: ...
def validate_block_number(value) -> None: ...

validate_block_hash: Incomplete
validate_transaction_hash: Incomplete
validate_filter_id: Incomplete

def validate_account(value) -> None: ...
def validate_inbound_storage_slot(value) -> None: ...
def is_valid_topic_array(value): ...
def validate_filter_params(from_block, to_block, address, topics): ...
def validate_private_key(value) -> None: ...

TRANSACTION_KEYS: Incomplete
SIGNED_TRANSACTION_KEYS: Incomplete
TRANSACTION_INTERNAL_TYPE_INFO: Incomplete
ALLOWED_TRANSACTION_INTERNAL_TYPES: Incomplete

def validate_transaction(value, txn_internal_type) -> None: ...
def validate_raw_transaction(raw_transaction) -> None: ...

INBOUND_WITHDRAWAL_VALIDATORS: Incomplete

def validate_inbound_withdrawals(withdrawals_list: list[dict[str, int | str | HexStr | bytes]]): ...
