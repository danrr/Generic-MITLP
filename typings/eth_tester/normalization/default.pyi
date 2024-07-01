from _typeshed import Incomplete

from .base import BaseNormalizer as BaseNormalizer
from .common import int_to_32byte_hex as int_to_32byte_hex
from .common import to_integer_if_hex as to_integer_if_hex

class DefaultNormalizer(BaseNormalizer):
    normalize_inbound_account: Incomplete
    normalize_inbound_block_hash: Incomplete
    normalize_inbound_block_number: Incomplete
    normalize_inbound_filter_id: Incomplete
    normalize_inbound_filter_params: Incomplete
    normalize_inbound_log_entry: Incomplete
    normalize_inbound_private_key: Incomplete
    normalize_inbound_raw_transaction: Incomplete
    normalize_inbound_storage_slot: Incomplete
    normalize_inbound_timestamp: Incomplete
    normalize_inbound_transaction: Incomplete
    normalize_inbound_transaction_hash: Incomplete
    normalize_outbound_account: Incomplete
    normalize_outbound_account_list: Incomplete
    normalize_outbound_balance: Incomplete
    normalize_outbound_block_hash: Incomplete
    normalize_outbound_block: Incomplete
    normalize_outbound_code: Incomplete
    normalize_outbound_filter_id: Incomplete
    normalize_outbound_log_entry: Incomplete
    normalize_outbound_gas_estimate: Incomplete
    normalize_outbound_nonce: Incomplete
    normalize_outbound_receipt: Incomplete
    normalize_outbound_return_data: Incomplete
    normalize_outbound_storage: Incomplete
    normalize_outbound_transaction: Incomplete
    normalize_outbound_transaction_hash: Incomplete
