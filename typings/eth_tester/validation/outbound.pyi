from _typeshed import Incomplete
from eth_tester.constants import UINT256_MAX as UINT256_MAX
from eth_tester.constants import UINT2048_MAX as UINT2048_MAX
from eth_tester.exceptions import ValidationError as ValidationError

from ..backends.pyevm.utils import is_cancun_block as is_cancun_block
from ..backends.pyevm.utils import is_london_block as is_london_block
from ..backends.pyevm.utils import is_shanghai_block as is_shanghai_block
from .common import if_not_create_address as if_not_create_address
from .common import if_not_null as if_not_null
from .common import validate_any as validate_any
from .common import validate_array as validate_array
from .common import validate_bytes as validate_bytes
from .common import validate_dict as validate_dict
from .common import validate_positive_integer as validate_positive_integer
from .common import validate_transaction_type as validate_transaction_type
from .common import validate_uint64 as validate_uint64
from .common import validate_uint256 as validate_uint256

def validate_32_byte_string(value) -> None: ...

validate_block_hash = validate_32_byte_string

def validate_nonce(value) -> None: ...
def validate_logs_bloom(value) -> None: ...
def validate_canonical_address(value) -> None: ...
def validate_log_entry_type(value) -> None: ...

LOG_ENTRY_VALIDATORS: Incomplete
validate_log_entry: Incomplete

def validate_signature_v(value) -> None: ...
def validate_y_parity(value) -> None: ...

LEGACY_TRANSACTION_VALIDATORS: Incomplete
validate_legacy_transaction: Incomplete
ACCESS_LIST_TRANSACTION_VALIDATORS: Incomplete
validate_access_list_transaction: Incomplete
DYNAMIC_FEE_TRANSACTION_VALIDATORS: Incomplete
validate_dynamic_fee_transaction: Incomplete
BLOB_TRANSACTION_VALIDATORS: Incomplete
validate_blob_transactions: Incomplete
validate_transaction: Incomplete
WITHDRAWAL_VALIDATORS: Incomplete
validate_withdrawal: Incomplete

def validate_status(value) -> None: ...

RECEIPT_VALIDATORS: Incomplete
CANCUN_RECEIPT_VALIDATORS: Incomplete
validate_receipt: Incomplete
BLOCK_VALIDATORS: Incomplete
validate_block: Incomplete
validate_accounts: Incomplete
