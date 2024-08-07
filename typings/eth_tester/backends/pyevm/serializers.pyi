from eth_tester.constants import ACCESS_LIST_TX_TYPE as ACCESS_LIST_TX_TYPE
from eth_tester.constants import BLOB_TX_TYPE as BLOB_TX_TYPE
from eth_tester.constants import DYNAMIC_FEE_TX_TYPE as DYNAMIC_FEE_TX_TYPE
from eth_tester.constants import GAS_PER_BLOB as GAS_PER_BLOB
from eth_tester.constants import LEGACY_TX_TYPE as LEGACY_TX_TYPE
from eth_tester.exceptions import ValidationError as ValidationError
from eth_tester.utils.address import generate_contract_address as generate_contract_address
from eth_tester.utils.encoding import int_to_32byte_big_endian as int_to_32byte_big_endian

from .utils import is_cancun_block as is_cancun_block
from .utils import is_london_block as is_london_block
from .utils import is_shanghai_block as is_shanghai_block
from .utils import is_supported_pyevm_version_available as is_supported_pyevm_version_available

def pad32(value): ...
def serialize_block(block, full_transaction, is_pending): ...
def serialize_transaction_hash(block, transaction, transaction_index, is_pending): ...
def serialize_transaction(block, transaction, transaction_index, is_pending): ...
def serialize_transaction_receipt(block, receipts, transaction, transaction_index, is_pending, vm): ...
def serialize_log(block, transaction, transaction_index, log, log_index, is_pending): ...
def serialize_block_withdrawals(block): ...
