from _typeshed import Incomplete
from eth_tester.utils.module_loading import get_import_path as get_import_path
from eth_tester.utils.module_loading import import_string as import_string

from .default import DefaultValidator as DefaultValidator

DEFAULT_VALIDATOR_CLASS: Incomplete

def get_validation_backend_class(backend_import_path): ...
def get_validator(backend_class: Incomplete | None = None): ...
