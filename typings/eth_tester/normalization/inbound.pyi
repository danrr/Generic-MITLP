from collections.abc import Generator

from _typeshed import Incomplete
from eth_tester.validation.inbound import is_32_bytes as is_32_bytes
from eth_tester.validation.inbound import is_32byte_hex_string as is_32byte_hex_string
from eth_tester.validation.inbound import is_valid_topic_array as is_valid_topic_array

from .common import normalize_array as normalize_array
from .common import normalize_dict as normalize_dict
from .common import normalize_if as normalize_if

def normalize_topic(topic): ...
def normalize_topic_list(topics) -> Generator[Incomplete, None, None]: ...
def normalize_filter_params(from_block, to_block, address, topics) -> Generator[Incomplete, None, None]: ...
def normalize_private_key(value): ...

to_empty_or_canonical_address: Incomplete
TRANSACTION_NORMALIZERS: Incomplete
normalize_transaction: Incomplete
LOG_ENTRY_NORMALIZERS: Incomplete
normalize_log_entry: Incomplete

def normalize_raw_transaction(raw_transaction_hex): ...
