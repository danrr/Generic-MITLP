"""
Sourced from https://github.com/Election-Tech-Initiative/electionguard-python/blob/main/stubs/gmpy2.pyi
Changed to make it work with pyright.

Stub of gympy2 mpz to support typecheck.

Created by running `stubgen -p gmpy2`, and then modifying the output manually
Necessary to support mypy typechecking
"""

from typing import Any, Literal, Optional, Text, TypeAlias, Union, overload

_PositiveInteger: TypeAlias = Literal[
    1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25
]
_NegativeInteger: TypeAlias = Literal[
    -1, -2, -3, -4, -5, -6, -7, -8, -9, -10, -11, -12, -13, -14, -15, -16, -17, -18, -19, -20
]

class mpz(int):
    def __new__(cls, x: Union[Text, bytes, bytearray, int], /, base: int = ...) -> mpz: ...
    def bit_clear(self, n: int) -> mpz: ...
    def bit_flip(self, n: int) -> mpz: ...
    def bit_length(self, *args: int, **kwargs: Any) -> int: ...
    def bit_scan0(self, n: int = ...) -> int: ...
    def bit_scan1(self, n: int = ...) -> int: ...
    def bit_set(self, n: int) -> mpz: ...
    def bit_test(self, n: int) -> bool: ...
    def digits(self) -> str: ...
    def is_divisible(self, d: int) -> bool: ...
    def is_even(self) -> bool: ...
    def is_odd(self) -> bool: ...
    def is_power(self) -> bool: ...
    def is_prime(self) -> bool: ...
    def is_square(self) -> bool: ...
    def num_digits(self, base: int = ...) -> int: ...
    def __abs__(self) -> mpz: ...
    def __add__(self, other: int) -> mpz: ...
    def __and__(self, other: int) -> mpz: ...
    def __bool__(self) -> bool: ...
    def __ceil__(self) -> mpz: ...
    def __divmod__(self, other: int) -> tuple[mpz, mpz]: ...
    def __eq__(self, other: object) -> bool: ...
    def __float__(self) -> mpz: ...  # maybe not mpz?
    def __floor__(self) -> mpz: ...
    def __floordiv__(self, other: int) -> mpz: ...
    def __format__(self, *args: Any, **kwargs: Any) -> str: ...
    def __ge__(self, other: int) -> bool: ...
    def __getitem__(self, index: int) -> mpz: ...
    def __gt__(self, other: int) -> bool: ...
    def __hash__(self) -> int: ...
    def __iadd__(self, other: int) -> mpz: ...
    def __ifloordiv__(self, other: int) -> mpz: ...
    def __ilshift__(self, other: int) -> mpz: ...
    def __imod__(self, other: int) -> mpz: ...
    def __imul__(self, other: int) -> mpz: ...
    def __index__(self) -> int: ...
    def __int__(self) -> int: ...
    def __invert__(self) -> mpz: ...
    def __irshift__(self, other: int) -> mpz: ...
    def __isub__(self, other: int) -> mpz: ...
    def __le__(self, other: int) -> bool: ...
    def __len__(self) -> int: ...
    def __lshift__(self, other: int) -> mpz: ...
    def __lt__(self, other: int) -> bool: ...
    def __mod__(self, other: int) -> mpz: ...
    def __mul__(self, other: int) -> mpz: ...
    def __ne__(self, other: object) -> bool: ...
    def __neg__(self) -> mpz: ...
    def __or__(self, other: int) -> mpz: ...
    def __pos__(self) -> bool: ...
    @overload
    def __pow__(self, other: Literal[0], mod: None = ..., /) -> Literal[1]: ...
    @overload
    def __pow__(self, other: _PositiveInteger, mod: None = ..., /) -> mpz: ...
    @overload
    def __pow__(self, other: _NegativeInteger, mod: None = ..., /) -> mpfr: ...
    @overload
    def __pow__(self, other: int, mod: int = ...) -> mpz: ...
    def __radd__(self, other: int) -> mpz: ...
    def __rand__(self, other: int) -> mpz: ...
    def __rdivmod__(self, other: int) -> tuple[mpz, mpz]: ...
    def __rfloordiv__(self, other: int) -> mpz: ...
    def __rlshift__(self, other: int) -> mpz: ...
    def __rmod__(self, other: int) -> mpz: ...
    def __rmul__(self, other: int) -> mpz: ...
    def __ror__(self, other: int) -> mpz: ...
    def __rpow__(self, other: int, __modulo: Optional[int] = ..., /) -> mpz: ...
    def __rrshift__(self, other: int) -> mpz: ...
    def __rshift__(self, other: int) -> mpz: ...
    def __rsub__(self, other: int) -> mpz: ...
    def __rtruediv__(self, other: float) -> mpfr: ...
    def __rxor__(self, other: int) -> mpz: ...
    def __sizeof__(self) -> int: ...
    def __sub__(self, other: int) -> mpz: ...
    def __truediv__(self, other: float) -> mpfr: ...
    def __trunc__(self) -> mpz: ...
    def __xor__(self, other: int) -> mpz: ...

class mpfr(float): ...

def invert(x: mpz, m: mpz) -> mpz: ...
def powmod(a: int, e: int, p: int) -> mpz: ...
def to_binary(a: mpz) -> bytes: ...
def from_binary(b: bytes) -> mpz: ...

RandomState: TypeAlias = type[object]

def random_state(seed: Optional[int] = None) -> RandomState: ...
def mpz_urandomb(state: RandomState, bits: int) -> mpz: ...
def mpz_random(state: RandomState, n: int) -> mpz: ...
def gcd(a: int, b: int) -> mpz: ...
def next_prime(p: int) -> mpz: ...
