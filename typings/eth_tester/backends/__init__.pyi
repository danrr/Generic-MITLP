from _typeshed import Incomplete
from eth_tester.utils.module_loading import get_import_path as get_import_path
from eth_tester.utils.module_loading import import_string as import_string

from .mock import MockBackend as MockBackend
from .pyevm import PyEVMBackend as PyEVMBackend
from .pyevm import is_supported_pyevm_version_available as is_supported_pyevm_version_available

def get_chain_backend_class(backend_import_path: Incomplete | None = None): ...
def get_chain_backend(backend_class: Incomplete | None = None): ...
