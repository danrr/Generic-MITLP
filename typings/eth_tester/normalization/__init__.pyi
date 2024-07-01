from _typeshed import Incomplete
from eth_tester.utils.module_loading import get_import_path as get_import_path
from eth_tester.utils.module_loading import import_string as import_string

from .default import DefaultNormalizer as DefaultNormalizer

DEFAULT_NORMALIZER_CLASS: Incomplete

def get_normalizer_backend_class(backend_import_path: Incomplete | None = None): ...
def get_normalizer_backend(backend_class: Incomplete | None = None): ...
