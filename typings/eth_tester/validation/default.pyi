from _typeshed import Incomplete

from .base import BaseValidator as BaseValidator
from .common import validate_uint256 as validate_uint256
from .outbound import validate_32_byte_string as validate_32_byte_string

class DefaultValidator(BaseValidator):
    validate_inbound_account: Incomplete
    validate_inbound_block_hash: Incomplete
    validate_inbound_block_number: Incomplete
    validate_inbound_filter_id: Incomplete
    validate_inbound_filter_params: Incomplete
    validate_inbound_private_key: Incomplete
    validate_inbound_raw_transaction: Incomplete
    validate_inbound_storage_slot: Incomplete
    validate_inbound_timestamp: Incomplete
    validate_inbound_transaction: Incomplete
    validate_inbound_transaction_hash: Incomplete
    validate_outbound_accounts: Incomplete
    validate_outbound_balance: Incomplete
    validate_outbound_block: Incomplete
    validate_outbound_block_hash: Incomplete
    validate_outbound_code: Incomplete
    validate_outbound_gas_estimate: Incomplete
    validate_outbound_nonce: Incomplete
    validate_outbound_log_entry: Incomplete
    validate_outbound_receipt: Incomplete
    validate_outbound_return_data: Incomplete
    validate_outbound_storage: Incomplete
    validate_outbound_transaction: Incomplete
    validate_outbound_transaction_hash: Incomplete
