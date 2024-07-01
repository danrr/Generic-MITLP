from _typeshed import Incomplete
from eth_utils.curried import to_checksum_address

from ..utils.encoding import int_to_32byte_big_endian as int_to_32byte_big_endian
from .common import normalize_array as normalize_array
from .common import normalize_dict as normalize_dict
from .common import normalize_if as normalize_if

normalize_account = to_checksum_address
normalize_account_list: Incomplete
to_empty_or_checksum_address: Incomplete
to_hex_if_integer: Incomplete
TRANSACTION_NORMALIZERS: Incomplete
normalize_transaction: Incomplete
WITHDRAWAL_NORMALIZERS: Incomplete
normalize_withdrawal: Incomplete

def is_transaction_hash_list(value): ...
def is_transaction_object_list(value): ...

BLOCK_NORMALIZERS: Incomplete
normalize_block: Incomplete
LOG_ENTRY_NORMALIZERS: Incomplete
normalize_log_entry: Incomplete
RECEIPT_NORMALIZERS: Incomplete
normalize_receipt: Incomplete
